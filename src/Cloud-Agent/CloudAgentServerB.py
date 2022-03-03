import asyncio
from datetime import date
import datetime
import json
import logging
import os
import random
import sys
import time
from uuid import uuid4
from aiohttp import ClientError
from aries_cloudagent.protocols.connections.v1_0.routes import ConnectionListSchema
from demo.runners.support.agent import CRED_FORMAT_JSON_LD, SIG_TYPE_BLS

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa

from runners.agent_container import (  # noqa:E402
    arg_parser,
    create_agent_with_args,
    AriesAgent,
)
from runners.support.utils import (  # noqa:E402
    check_requires,
    log_msg,
    log_status,
    log_timer,
    prompt,
    prompt_loop,
)

############# TODO #######################
# 
# 

# Type de Credentials
# CRED_PREVIEW_TYPE = "https://didcomm.org/issue-credential/2.0/credential-preview"
# SELF_ATTESTED = os.getenv("SELF_ATTESTED")
# TAILS_FILE_COUNT = int(os.getenv("TAILS_FILE_COUNT", 100))


TAILS_FILE_COUNT = int(os.getenv("TAILS_FILE_COUNT", 100))
CRED_PREVIEW_TYPE = (
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/credential-preview"
)


logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(__name__)


class AcmeAgent(AriesAgent):
    def __init__(
        self,
        ident: str,
        http_port: int,
        admin_port: int,
        no_auto: bool = False,
        **kwargs,
    ):
        super().__init__(
            ident,
            http_port,
            admin_port,
            prefix="Acme",
            no_auto=no_auto,
            **kwargs,
        )
        self.connection_id = None
        self._connection_ready = None
        self.cred_state = {}
        self.cred_attrs = {}

    async def detect_connection(self):
        await self._connection_ready
        self._connection_ready = None

    @property
    def connection_ready(self):
        return self._connection_ready.done() and self._connection_ready.result()

    async def handle_oob_invitation(self, message):
        pass

    ########## TODO ###############
    # def generate_credential_offer(self, aip, cred_type, cred_def_id):
    #     d = datetime.date.today()
        
    #     offer_request = {
    #                 "connection_id": self.get_public_did,
    #                 "filter": {
    #                     "ld_proof": {
    #                         "credential": {
    #                             "@context": [
    #                                 "https://www.w3.org/2018/credentials/v1",
    #                                 "https://w3id.org/citizenship/v1",
    #                                 "https://w3id.org/security/bbs/v1",
    #                             ],
    #                             "type": [
    #                                 "VerifiableCredential",
    #                                 "PermanentResident",
    #                             ],
    #                             "id": "https://credential.example.com/residents/1234567890",
    #                             "issuer": self.did,
    #                             "issuanceDate": "2020-01-01T12:00:00Z",
    #                             "credentialSubject": {
    #                                 "type": ["PermanentResident"],
    #                                 "givenName": "ALICE",
    #                                 "familyName": "SMITH",
    #                                 "gender": "Female",
    #                                 "birthCountry": "Bahamas",
    #                                 "birthDate": "1958-07-17",
    #                             },
    #                         },
    #                         "options": {"proofType": SIG_TYPE_BLS},
    #                     }
    #                 },
                
    #         }
    #     return offer_request


    async def handle_connections(self, message):
        print(
            self.ident, "handle_connections", message["state"], message["rfc23_state"]
        )
        conn_id = message["connection_id"]
        if (not self.connection_id) and message["rfc23_state"] == "invitation-sent":
            print(self.ident, "set connection id", conn_id)
            self.connection_id = conn_id
        if (
            message["connection_id"] == self.connection_id
            and message["rfc23_state"] == "completed"
            and (self._connection_ready and not self._connection_ready.done())
        ):
            self.log("Connected")
            self._connection_ready.set_result(True)

    async def handle_issue_credential_v2_0(self, message):
        state = message["state"]
        cred_ex_id = message["cred_ex_id"]
        prev_state = self.cred_state.get(cred_ex_id)
        if prev_state == state:
            return  # ignore
        self.cred_state[cred_ex_id] = state

        self.log(f"Credential: state = {state}, cred_ex_id = {cred_ex_id}")

        # If we receive a request, issue and POST a credential
        if state == "request-received":
            # issue credentials based on offer preview in cred ex record
            if not message.get("auto_issue"):
                await self.admin_POST(
                    f"/issue-credential-2.0/records/{cred_ex_id}/issue",
                    {"comment": f"Issuing credential, exchange {cred_ex_id}"},
                )
            

    async def handle_issue_credential_v2_0_indy(self, message):
        pass  # employee id schema does not support revocation

    async def handle_present_proof_v2_0(self, message):
        state = message["state"]
        pres_ex_id = message["pres_ex_id"]
        self.log(f"Presentation: state = {state}, pres_ex_id = {pres_ex_id}")

        if state == "presentation-received":
            # TODO handle received presentations
            pass

    async def handle_basicmessages(self, message):
        self.log("Received message:", message["content"])


async def main(args):
    acme_agent = await create_agent_with_args(args, ident="acme")

    try:
        log_status(
            "#1 Provision an agent and wallet, get back configuration details"
            + (
                f" (Wallet type: {acme_agent.wallet_type})"
                if acme_agent.wallet_type
                else ""
            )
        )
        agent = AcmeAgent(
            "acme.agent",
            acme_agent.start_port,
            acme_agent.start_port + 1,
            genesis_data=acme_agent.genesis_txns,
            genesis_txn_list=acme_agent.genesis_txn_list,
            no_auto=acme_agent.no_auto,
            tails_server_base_url=acme_agent.tails_server_base_url,
            timing=acme_agent.show_timing,
            multitenant=acme_agent.multitenant,
            mediation=acme_agent.mediation,
            wallet_type=acme_agent.wallet_type,
            seed=acme_agent.seed,
        )

        acme_agent.public_did = True
        acme_schema_name = "publickey"
        acme_schema_attrs = ["publickey", "date", "timestamp"]
        await acme_agent.initialize(
            the_agent=agent,
            schema_name = acme_schema_name,
            schema_attrs=acme_schema_attrs,
        )

        with log_timer("Publish schema and cred def duration:"):
            # define schema
            # version = format(
            #     "%d %d"
            #     % (
            #         random.randint(1, 101),
            #         random.randint(1, 101),
            #     )
            # )
            version = "2.0"
           


            # register schema and cred def
            (schema_id, cred_def_id) = await agent.register_schema_and_creddef(
                "publickey schema",
                version,
                ["publickey", "date", "timestamp"],
                support_revocation=False,
                revocation_registry_size=TAILS_FILE_COUNT,
            )
        
        # generate an invitation for Alice
        await acme_agent.generate_invitation(display_qr=True, wait=True)

        options = (
            "    (1) Issue Credential\n"
            "    (2) Send Proof Request\n"
            "    (3) Send Message\n"
            "    (4) Generate New Invitation\n"
            "    (X) Exit?\n"
            "[1/2/3/4/X]"
        )
        async for option in prompt_loop(options):
            if option is not None:
                option = option.strip()

            if option is None or option in "xX":
                break

            # Option 1 : Issue a credential to our client
            elif option == "1":
                log_status("#13 Issue credential offer to X")

################### METHOD 1 ISSUE VC ####################3

                # offer_request = acme_agent.agent.generate_credential_offer(
                #             acme_agent.aip,
                #             acme_agent.cred_type,
                #             None,
                #             #agent.exchange_tracing,
                #         )
                # await acme_agent.agent.admin_POST(
                #         "/issue-credential-2.0/send-offer", offer_request
                #     )

 ############### METHOD 2 ################################

                # Credential attributes
                agent.cred_attrs[cred_def_id] = {
                    "publickey": agent.connection_id,
                    "date": date.isoformat(date.today()),
                    "timestamp": str(int(time.time())),
                }

                # Create a preview
                cred_preview = {
                    "@type": CRED_PREVIEW_TYPE,
                    "attributes": [
                        {"name": n, "value": v}
                        for (n, v) in agent.cred_attrs[cred_def_id].items()
                    ],
                }

                # Complete VC
                offer_request = {
                    "connection_id": agent.connection_id,
                    "comment": f"Offer on cred def id {cred_def_id}",
                    "credential_preview": cred_preview,
                    "filter": {"indy": {"cred_def_id": cred_def_id}},
                }
                
                await agent.admin_POST(
                    "/issue-credential-2.0/send-offer", offer_request
                )
                
                             

            elif option == "2":
                log_status("#20 Request proof from alice")
                req_attrs = [
                    {
                        "name": "publickey",
                        "restrictions": [{"schema_name": "publickey schema"}]
                    },
                    {
                        "name": "date",
                        "restrictions": [{"schema_name": "publickey schema"}]
                    },
                    {
                        "name": "timestamp",
                        "restrictions": [{"schema_name": "publickey schema"}]
                    }
                ]
                req_preds = []
                indy_proof_request = {
                    "name": "Proof ",
                    "version": "2.0",
                    "nonce": str(uuid4().int),
                    "requested_attributes": {
                        f"0_{req_attr['name']}_uuid": req_attr
                        for req_attr in req_attrs
                    },
                    "requested_predicates": {}
                }
                proof_request_web_request = {
                    "connection_id": agent.connection_id,
                    "presentation_request": {"indy": indy_proof_request},
                }
                # this sends the request to our agent, which forwards it to Alice
                # (based on the connection_id)
                await agent.admin_POST(
                    "/present-proof-2.0/send-request",
                    proof_request_web_request
                )

            elif option == "3":
                msg = await prompt("Enter message: ")
                await agent.admin_POST(
                    f"/connections/{agent.connection_id}/send-message", {"content": msg}
                )

            elif option == "4":
                log_msg(
                    "Creating a new invitation, please receive "
                    "and accept this invitation using Alice agent"
                )
                await acme_agent.generate_invitation(
                    display_qr=True,
                    reuse_connections=acme_agent.reuse_connections,
                    wait=True,
                )

        if acme_agent.show_timing:
            timing = await acme_agent.agent.fetch_timing()
            if timing:
                for line in acme_agent.agent.format_timing(timing):
                    log_msg(line)

    finally:
        terminated = await acme_agent.terminate()

    await asyncio.sleep(0.1)

    if not terminated:
        os._exit(1)


if __name__ == "__main__":
    parser = arg_parser(ident="acme", port=8040)
    args = parser.parse_args()

    ENABLE_PYDEVD_PYCHARM = os.getenv("ENABLE_PYDEVD_PYCHARM", "").lower()
    ENABLE_PYDEVD_PYCHARM = ENABLE_PYDEVD_PYCHARM and ENABLE_PYDEVD_PYCHARM not in (
        "false",
        "0",
    )
    PYDEVD_PYCHARM_HOST = os.getenv("PYDEVD_PYCHARM_HOST", "localhost")
    PYDEVD_PYCHARM_CONTROLLER_PORT = int(
        os.getenv("PYDEVD_PYCHARM_CONTROLLER_PORT", 5001)
    )

    if ENABLE_PYDEVD_PYCHARM:
        try:
            import pydevd_pycharm

            print(
                "Acme remote debugging to "
                f"{PYDEVD_PYCHARM_HOST}:{PYDEVD_PYCHARM_CONTROLLER_PORT}"
            )
            pydevd_pycharm.settrace(
                host=PYDEVD_PYCHARM_HOST,
                port=PYDEVD_PYCHARM_CONTROLLER_PORT,
                stdoutToServer=True,
                stderrToServer=True,
                suspend=False,
            )
        except ImportError:
            print("pydevd_pycharm library was not found")

    check_requires(args)

    try:
        asyncio.get_event_loop().run_until_complete(main(args))
    except KeyboardInterrupt:
        os._exit(1)
