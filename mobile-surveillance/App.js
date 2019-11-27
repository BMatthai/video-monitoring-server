import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import Button from 'react-native-button';
import { pjsipHelper } from './js/pjsip-helper';

export default function App() {
  return (
    <View style={styles.container}>
      <Button
          onPress={() => pjsipHelper.start() }>
          S‘enregistrer
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

