import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import PjsipHelper from 'PjsipHelper';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Open up App.js to start working on your app!</Text>
      <button onClick={this.handleClick}>Bouton</button>
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
