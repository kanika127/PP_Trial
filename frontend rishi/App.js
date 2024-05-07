import * as React from 'react';
import { StatusBar } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useFonts } from 'expo-font';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import TabNavigator from './screens/navigation/TabNavigator';
import ProfileStackNavigator from './screens/navigation/ProfileStackNavigator';
import { enableScreens } from 'react-native-screens';

enableScreens();

// Screens
import Page from './screens/Page';
import Page1 from './screens/Page1';
import Page2 from './screens/Page2';
import TwoFactorAuthScreen from './screens/2factor';
import LoginPage from './screens/LoginPage';
import Industry1 from './screens/Industry1';
import Industry2 from './screens/Industry2';

const AuthStack = createNativeStackNavigator();
const RootStack = createNativeStackNavigator();

// Stack navigator for auth flow
function AuthStackNavigator() {
  return (
    <AuthStack.Navigator screenOptions={{ headerShown: false }} initialRouteName="Page">
      <AuthStack.Screen name="Page" component={Page} />
      <AuthStack.Screen name="Page1" component={Page1} />
      <AuthStack.Screen name="Page2" component={Page2} />
      <AuthStack.Screen name="TwoFactorAuthScreen" component={TwoFactorAuthScreen} />
      <AuthStack.Screen name="LoginPage" component={LoginPage} />
      <AuthStack.Screen name="Industry1" component={Industry1} />
      <AuthStack.Screen name="Industry2" component={Industry2} />
    </AuthStack.Navigator>
  );
}

// Root stack navigator
function RootStackNavigator() {
  return (
    <RootStack.Navigator screenOptions={{ headerShown: false }}>
      <RootStack.Screen name="Auth" component={AuthStackNavigator} />
      <RootStack.Screen name="MainApp" component={TabNavigator} />
      <RootStack.Screen name="ProfileFlow" component={ProfileStackNavigator} /> 
    </RootStack.Navigator>
  );
}

const App = () => {
  const [fontsLoaded] = useFonts({
    'HelveticaNeue-Light': require('./assets/fonts/HelveticaNeue-Light.otf'),
    'Poppins-Medium': require('./assets/fonts/Poppins-Medium.ttf'),
  });

  if (!fontsLoaded) {
    return null; // Optionally, return a splash screen here
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <NavigationContainer>
        <RootStackNavigator />
      </NavigationContainer>
    </GestureHandlerRootView>
  );
};

export default App;
