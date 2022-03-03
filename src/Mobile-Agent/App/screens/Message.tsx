import React from 'react'
import {StackNavigationProp} from "@react-navigation/stack";
import {MessageStackParams} from "types/navigators";

interface MessageProps {
    navigation: StackNavigationProp<MessageStackParams>
}
const Message: React.FC<MessageProps> = ({ navigation }) => {
    return (
       <view>
           <text>Wellcome on message</text>
       </view>
    )
}

export default Message
