import React, { useMemo } from "react";
import { Image } from "expo-image";
import { StyleSheet, Text, View } from "react-native";
import { FontSize, FontFamily, Color, Border } from "../GlobalStyles";

const getStyleValue = (key, value) => {
  if (value === undefined) return;
  return { [key]: value === "unset" ? undefined : value };
};
const DarkModeTrueTypeDefault = ({
  darkModeTrueTypeDefaultPosition,
  darkModeTrueTypeDefaultMarginLeft,
  darkModeTrueTypeDefaultTop,
  darkModeTrueTypeDefaultLeft,
}) => {
  const darkModeTrueTypeDefaultStyle = useMemo(() => {
    return {
      ...getStyleValue("position", darkModeTrueTypeDefaultPosition),
      ...getStyleValue("marginLeft", darkModeTrueTypeDefaultMarginLeft),
      ...getStyleValue("top", darkModeTrueTypeDefaultTop),
      ...getStyleValue("left", darkModeTrueTypeDefaultLeft),
    };
  }, [
    darkModeTrueTypeDefaultPosition,
    darkModeTrueTypeDefaultMarginLeft,
    darkModeTrueTypeDefaultTop,
    darkModeTrueTypeDefaultLeft,
  ]);

  return (
    <View
      style={[styles.darkModetrueTypedefault, darkModeTrueTypeDefaultStyle]}
    >
      <Image
        style={styles.notchIcon}
        contentFit="cover"
        source={require("../assets/notch.png")}
      />
      <View style={[styles.leftSide, styles.leftSideLayout]}>
        <View style={[styles.statusbarTime, styles.leftSideLayout]}>
          <Text style={[styles.text, styles.textPosition]}>9:41</Text>
        </View>
      </View>
      <View style={[styles.rightSide, styles.rightSidePosition]}>
        <Image
          style={[styles.batteryIcon, styles.rightSidePosition]}
          contentFit="cover"
          source={require("../assets/battery.png")}
        />
        <Image
          style={styles.wifiIcon}
          contentFit="cover"
          source={require("../assets/wifi.png")}
        />
        <Image
          style={[styles.iconMobileSignal, styles.textPosition]}
          contentFit="cover"
          source={require("../assets/icon--mobile-signal.png")}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  leftSideLayout: {
    height: 21,
    width: 54,
    left: "50%",
    position: "absolute",
  },
  textPosition: {
    top: 1,
    position: "absolute",
  },
  rightSidePosition: {
    height: 13,
    left: "50%",
    position: "absolute",
  },
  notchIcon: {
    marginLeft: -82,
    top: -2,
    width: 164,
    height: 32,
    left: "50%",
    position: "absolute",
  },
  text: {
    left: 0,
    fontSize: FontSize.size_mid,
    letterSpacing: 0,
    lineHeight: 22,
    fontWeight: "600",
    fontFamily: FontFamily.sourceSansPro,
    color: Color.colorWhite,
    textAlign: "center",
    height: 20,
    width: 54,
    top: 1,
  },
  statusbarTime: {
    marginLeft: -27,
    borderRadius: Border.br_5xl,
    top: 0,
  },
  leftSide: {
    marginLeft: -168,
    top: 14,
  },
  batteryIcon: {
    marginLeft: 11.3,
    width: 27,
    top: 0,
  },
  wifiIcon: {
    width: 17,
    height: 12,
  },
  iconMobileSignal: {
    marginLeft: -38.7,
    width: 18,
    height: 12,
    left: "50%",
  },
  rightSide: {
    marginLeft: 91,
    top: 19,
    width: 77,
  },
  darkModetrueTypedefault: {
    width: 390,
    height: 47,
    overflow: "hidden",
  },
});

export default DarkModeTrueTypeDefault;
