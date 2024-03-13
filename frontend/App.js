/*
import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Open up App.js to start working on your app!</Text>
	<Text>Vandana Agrwal</Text>
      <StatusBar style="auto" />
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
*/

import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import axios from 'axios';
export default function App() {

const [message, setMessage] = useState('');

useEffect(() => {

//axios.get('http://localhost:8000/app1/hello/')
fetch('http://localhost:8000/app1/hello/')
	//.then(response => {response.json() ;
	//.then(json => console.log(json))) ;

.then(response => {

document.write('MY mesg ---> Vandana Agarwal'); //----> THIS WORKS
//setMessage(response.data.message);
document.write(response.json());

})

.catch(error => {

console.log(error);

});

}, []);

return (

<View style={styles.container}>

<Text>{message}</Text>

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

/*
import React from 'react';
import {Text, View} from 'react-native';

type nameObj
const Name = (props) => {
	return (
		<View>
		<Text>props</Text>
		</View>
	) ;
} ;

const HelloWorldApp = () => {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
      }}>
      <Text>Hello, world!</Text>
	  <Name />
	  <Vandana/>
    </View>
  );
};

export default HelloWorldApp;
*/
