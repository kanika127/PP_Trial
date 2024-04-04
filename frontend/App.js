import React, { useState } from 'react';
import {
  StyleSheet,
  SafeAreaView,
  View,
  Image,
  Text,
  TouchableOpacity,
  TextInput,
} from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
// Import light blue passion project logo
import LightBlueTrim from './assets/lightblue-trim.png'

export default function Example() {
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    mobile: '',
    password: '',
  });
  const [buttonPressed, setButtonPressed] = useState(false); // State variable for button press
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#292b2d' }}>
      <View style={styles.container}>
        <KeyboardAwareScrollView>
          <View style={styles.header}>
            <Image
              alt="App Logo"
              resizeMode="contain"
              style={styles.headerImg}
              source={LightBlueTrim} />

            <Text style={styles.title}>
              Sign in to <Text style={{ color: '#6ab4db' }}>Passion Project</Text>
            </Text>

            <Text style={styles.subtitle}>
              Find local project opportunities
            </Text>
          </View>

          <View style={styles.form}>
            <View style={styles.input}>
              <Text style={styles.inputLabel}>First Name</Text>

              <TextInput
                autoCapitalize="none"
                autoCorrect={false}
                keyboardType="first-name"
                onChangeText={first_name => setForm({ ...form, first_name })}
                // placeholder="rishabh@passionproject.nyc"
                placeholderTextColor="#6b7280"
                style={styles.inputControl}
                value={form.first_name} 
                id="first_name" />
            </View>

            <View style={styles.input}>
              <Text style={styles.inputLabel}>Last Name</Text>

              <TextInput
                autoCapitalize="none"
                autoCorrect={false}
                keyboardType="last-name"
                onChangeText={last_name => setForm({ ...form, last_name })}
                // placeholder="rishabh@passionproject.nyc"
                placeholderTextColor="#6b7280"
                style={styles.inputControl}
                value={form.last_name} 
                id="last_name" />
            </View>

            <View style={styles.input}>
              <Text style={styles.inputLabel}>Email address</Text>

              <TextInput
                autoCapitalize="none"
                autoCorrect={false}
                keyboardType="email-address"
                onChangeText={email => setForm({ ...form, email })}
                // placeholder="rishabh@passionproject.nyc"
                placeholderTextColor="#6b7280"
                style={styles.inputControl}
                value={form.email} 
                id="email" />
            </View>

            <View style={styles.input}>
              <Text style={styles.inputLabel}>Mobile Number</Text>

              <TextInput
                autoCapitalize="none"
                autoCorrect={false}
                keyboardType="mobile-number"
                onChangeText={mobile => setForm({ ...form, mobile })}
                // placeholder=""
                placeholderTextColor="#6b7280"
                style={styles.inputControl}
                value={form.mobile} 
                id="mobile" />
            </View>

            <View style={styles.input}>
              <Text style={styles.inputLabel}>Username</Text>

              <TextInput
                autoCapitalize="none"
                autoCorrect={false}
                keyboardType="username"
                onChangeText={username => setForm({ ...form, username })}
                // placeholder=""
                placeholderTextColor="#6b7280"
                style={styles.inputControl}
                value={form.username} 
                id="username" />
            </View>

            <View style={styles.input}>
              <Text style={styles.inputLabel}>Password</Text>

              <TextInput
                autoCorrect={false}
                onChangeText={password => setForm({ ...form, password })}
                // placeholder="********"
                placeholderTextColor="#6b7280"
                style={styles.inputControl}
                secureTextEntry={true}
                value={form.password}
                id="password" />
            </View>

            <View style={styles.formAction}>
            <TouchableOpacity
              onPress={() => {
                // handle onPress
                setButtonPressed(true); // Set buttonPressed to true when pressed
                fetch('http://localhost:8000/app1/register/', { // 'signup' / 'login' / 'reset_pass'
                    method: 'POST',
                    body: JSON.stringify({  
                        // username: 'rishi',
                        first_name: document.getElementById('first_name').value,
                        last_name: document.getElementById('last_name').value,
                        email: document.getElementById('email').value,
                        mobile: document.getElementById('mobile').value,
                        username: document.getElementById('username').value,
                        password: document.getElementById('password').value,
                        role: "Creator",
                    }),
                    headers: {
                        'Content-Type': 'application/json',
                        // Include any other headers your Django app requires
                    },
                })
                .then(response => {
                if (!response.ok) {
                  console.log("throwing response");
                  throw response;  // If response status code is not OK, throw the response for further handling
                }
                return response.json();})  // If OK, parse the response as JSON
                .then(data => {
                    console.log('Success:', data);
                })
                .catch(errorResponse => {
                  // Handle errors
                  if (errorResponse.status === 400) {  // Check if the error status code is 400
                    errorResponse.json().then(errorData => {
                      console.error('Validation Error:', errorData.error);  // Process and display the validation error
                      // Update the UI accordingly, e.g., display error messages next to form fields
                    });
                  } else {
                    console.error('Network or other error');
                  }
                });
            }}
            activeOpacity={0.8} // Set the opacity of the button when pressed
            style={[
             styles.btn,
            buttonPressed && styles.btnPressed // Apply btnPressed style when buttonPressed is true
             ]}>
             <Text style={styles.btnText}>Sign in</Text>
            </TouchableOpacity>
            </View>
            <Text style={styles.formLink}>Forgot password?</Text>
          </View>
        </KeyboardAwareScrollView>

        <TouchableOpacity
          onPress={() => {
            // handle link
          }}
          style={{ marginTop: 'auto' }}>
          <Text style={styles.formFooter}>
            Don't have an account?{' '}
            <Text style={{ textDecorationLine: 'underline' }}>Sign up</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: 24,
    paddingHorizontal: 0,
    flexGrow: 1,
    flexShrink: 1,
    flexBasis: 0,
  },
  title: {
    fontSize: 31,
    fontWeight: '700',
    color: '#f6e3cb',
    marginBottom: 7,
  },
  subtitle: {
    fontSize: 15,
    fontWeight: '500',
    color: '#f6e3cb',
  },
  /** Header */
  header: {
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 0,
  },
  headerImg: {
    width: 300,
    height: 300,
    alignSelf: 'center',
    marginBottom: 0,
  },
  /** Form */
  form: {
    marginBottom: 24,
    paddingHorizontal: 24,
    flexGrow: 1,
    flexShrink: 1,
    flexBasis: 0,
  },
  formAction: {
    marginTop: 4,
    marginBottom: 16,
  },
  formLink: {
    fontSize: 16,
    fontWeight: '600',
    color: '#6ab4db',
    textAlign: 'center',
  },
  formFooter: {
    fontSize: 15,
    fontWeight: '600',
    color: '#222',
    textAlign: 'center',
    letterSpacing: 0.15,
  },
  /** Input */
  input: {
    marginBottom: 16,
  },
  inputLabel: {
    fontSize: 17,
    fontWeight: '600',
    color: '#f6e3cb',
    marginBottom: 4,
    marginTop: 20,
  },
  inputControl: {
    height: 50,
    backgroundColor: '#fff',
    paddingHorizontal: 16,
    borderRadius: 12,
    fontSize: 15,
    fontWeight: '500',
    color: '#222',
    borderWidth: 1,
    borderColor: '#C9D3DB',
    borderStyle: 'solid',
  },
  /** Button */
  btn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 30,
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderWidth: 1,
    backgroundColor: '#6ab4db',
    borderColor: '#f6e3cb',
  },
  btnText: {
    fontSize: 18,
    lineHeight: 26,
    fontWeight: '600',
    color: '#fff',
  },
  btnPressed: {
    shadowColor: '#f6e3cb', // Change to the glowing color you desire
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 1,
    shadowRadius: 10,
    elevation: 5,
  },  
});



// /*
// import { StatusBar } from 'expo-status-bar';
// import React from 'react';
// import { StyleSheet, Text, View } from 'react-native';

// export default function App() {
//   return (
//     <View style={styles.container}>
//       <Text>Open up App.js to start working on your app!</Text>
// 	<Text>Vandana Agrwal</Text>
//       <StatusBar style="auto" />
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     backgroundColor: '#fff',
//     alignItems: 'center',
//     justifyContent: 'center',
//   },
// });
// */

// import React, { useEffect, useState } from 'react';
// import { StyleSheet, Text, View } from 'react-native';
// export default function App() {

// const [message, setMessage] = useState('');
// const [time, setTime] = useState('');

// useEffect(() => {

// fetch('http://localhost:8000/app1/hello/')
// 	//.then(response => {response.json() ;
// 	//.then(json => console.log(json))) ;

// .then(response => response.json())
// .then(json => {
// 	setMessage(json['message']) ;
// 	setTime(json['date']) ;
// 	console.log(json) ;

// })

// //document.write('MY mesg ---> Vandana Agarwal'); //----> THIS WORKS
// //setMessage(response.data.message);
// //document.write(response.json());

// //})

// .catch(error => {

// console.log(error);

// });

// }, []);

// return (

// <View style={styles.container}>

// <Text>{time}</Text>
// <Text>{message}</Text>
// <a href="http://localhost:8000/app1/add_creator">ADD new Creator</a>
// <a href="http://localhost:8000/app1/signup_creator">CREATOR SIGNUP</a>

// <a href="http://localhost:8000/app1/add_client">ADD new Client</a>
// <a href="http://localhost:8000/app1/signup_client">Client SIGNUP</a>
// </View>

// );

// }

// const styles = StyleSheet.create({

// container: {

// flex: 1,

// backgroundColor: '#fff',

// alignItems: 'center',

// justifyContent: 'center',

// },

// });

// /*
// import React from 'react';
// import {Text, View} from 'react-native';

// type nameObj
// const Name = (props) => {
// 	return (
// 		<View>
// 		<Text>props</Text>
// 		</View>
// 	) ;
// } ;

// const HelloWorldApp = () => {
//   return (
//     <View
//       style={{
//         flex: 1,
//         justifyContent: 'center',
//         alignItems: 'center',
//       }}>
//       <Text>Hello, world!</Text>
// 	  <Name />
// 	  <Vandana/>
//     </View>
//   );
// };

// export default HelloWorldApp;
// */
