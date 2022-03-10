# Aries Mobile Agent React Native

Aries Mobile Agent React Native est une application d'agent mobile Aries open source (Licence Apache2), qu'on a cloné et modifié par rapport à la version originale qui se trouve [ici](https://github.com/hyperledger/aries-mobile-agent-react-native)
. Il s'agit d'un projet qui a été créé pour concentrer les efforts de la communauté vers un projet open source central.

## Installation
Prérequis:
1. Node (la version 16.14.x est conseillée), Docker, Android Studio.
2. Suivez les étapes d'installation en fonction de votre OS :
   - La documentation de react: [react-native](https://reactnative.dev/docs/environment-setup).
   - Assurer vous de bien brancher un smartphone Android (Activer le mode développeur)
3. Déplacez vous dans le dossier Mobile-Agent :
   ```sh
   cd src/Mobile-Agent
   npm install
   npm install @react-navigation/bottom-tabs
   ```
## Run

- Dans un terminal lancez le metro bundler :
  ```sh
  npm run start
  ```
- Dans un autre terminal lancez :
     ```sh
  npm run android
  ```
## Générer une APK
- Si vous voulez crée une apk, c'est par [ici](https://medium.com/geekculture/react-native-generate-apk-debug-and-release-apk-4e9981a2ea51) 😎 