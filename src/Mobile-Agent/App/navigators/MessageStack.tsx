import React from "react";
import {SafeAreaView, StyleSheet, TextInput, Button, Alert} from "react-native";

const MessageStack: React.FC = () => {
    const [text, onChangeText] = React.useState("");

    return (
        <SafeAreaView style={styles.fixToText}>
            <TextInput
                style={styles.input}
                onChangeText={onChangeText}
                value={text}
                placeholder="Votre message"
            />
            <Button
                title="Envoyer"
                onPress={() => Alert.alert('Envoyer')}
            />
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    input: {
        height: 40,
        margin: 12,
        borderWidth: 1,
        padding: 10,
    },
    fixToText: {
        textAlign: 'center',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginTop: 30,
        marginRight: 10
    },
});

export default MessageStack;