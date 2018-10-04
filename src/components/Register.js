import React from 'react';
import { 
    Text,
    View, 
    Image, 
    StyleSheet, 
    KeyboardAvoidingView,
    LayoutAnimation,
    Platform,
    UIManager,
} from 'react-native';
import { BlurView } from 'expo';
import { Divider } from 'react-native-elements';
import { connect } from 'react-redux'; 
import { InputIcon, Button, Spinner } from './common';
import {
    authNameChange,
    authPhoneChange,
    authEmailChange,
    authPasswordChange,
    authCreateUser,
} from '../actions';

class Register extends React.Component {

    state = {
        secureTextEntry: true,
    };

    componentWillUpdate() {
        LayoutAnimation.easeInEaseOut();
    }

    onNameChange(text) {
        this.props.authNameChange(text);
    }

    onPhoneChange(text) {
        this.props.authPhoneChange(text);
    }

    onEmailChange(text) {
        this.props.authEmailChange(text);
    }

    onPasswordChange(text) {
        this.props.authPasswordChange(text);
    }

    onCreateUser() {
        const { email, password } = this.props;
        this.props.authCreateUser(email, password);
    }

    renderButton() {
        const { loading, error } = this.props;
        if (loading) {
            return (
                <Spinner />
            );
        }
        return (
            <View style={{ width: '100%' }}>
                <Text style={styles.errorText}>{error}</Text>
                <Button 
                    color='#EF4036'
                    onPress={this.onCreateUser.bind(this)}
                >
                    ลงทะเบียน
                </Button>
            </View>
        );
    }

    render() {
        const { container, cardStyle } = styles;
        const { secureTextEntry } = this.state;
        if (Platform.OS === 'android') {
            // UIManager.setLayoutAnimationEnabledExperimental && 
            UIManager.setLayoutAnimationEnabledExperimental(true);
        }

        return (
            <View style={{ flex: 1 }}>
                <Image
                    resizeMode='cover'
                    style={{
                        width: '100%',
                        height: '100%',
                    }}
                    source={require('../images/bg_free.png')} 
                />
                <BlurView tint="dark" intensity={40} style={StyleSheet.absoluteFill}>
                    <KeyboardAvoidingView style={container} behavior="padding">
                        <View style={cardStyle}>
                            <Text style={{ fontSize: 16 }}>กรุณากรอกข้อมูลด้านล่าง</Text>
                            <InputIcon
                                placeholder='ชื่อ-สกุล'
                                iconName='account-circle'
                                type='meterial-community'
                                addStyle={{ marginHorizontal: '5%' }}
                                onChangeText={this.onNameChange.bind(this)}
                                value={this.props.name}
                            />
                            <InputIcon
                                placeholder='เบอร์โทรศัพท์'
                                iconName='phone'
                                type='meterial-community'
                                addStyle={{ marginHorizontal: '5%' }}
                                onChangeText={this.onPhoneChange.bind(this)}
                                value={this.props.phone}
                            />
                            <InputIcon
                                placeholder='อีเมล'
                                iconName='mail'
                                type='meterial-community'
                                addStyle={{ marginHorizontal: '5%' }}
                                onChangeText={this.onEmailChange.bind(this)}
                                value={this.props.email}
                            />
                            <InputIcon
                                placeholder='รหัสผ่าน'
                                iconName='lock'
                                type='meterial-community'
                                addStyle={{ marginHorizontal: '5%' }}
                                secureTextEntry={secureTextEntry}
                                password
                                onChangeText={this.onPasswordChange.bind(this)}
                                onPress={() => 
                                    this.setState({ secureTextEntry: !secureTextEntry, })}
                                value={this.props.password}
                            />
                            <Divider style={{ height: 10 }} />
                            {this.renderButton()}
                        </View>
                    </KeyboardAvoidingView>
                </BlurView>
            </View>
        );
    }
}

const styles = {
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(0,0,0,0.5)',
    },
    cardStyle: {
        width: '80%',
        backgroundColor: '#FFA80D',
        paddingVertical: 20,
        borderRadius: 15,
        alignItems: 'center',
    },
    errorText: {
        alignSelf: 'center', 
        paddingBottom: 10, 
        color: '#EF4036', 
        shadowColor: 'black', 
        shadowOpacity: 0.2, 
        shadowOffset: { width: 1, height: 1 }, 
        textAlign: 'center',
    }
};

const mapStateToProps = ({ auth }) => {
    const { name, phone, email, password, loading, error } = auth;
    console.log(auth);
    return { name, phone, email, password, loading, error };
};

export default connect(mapStateToProps, {
    authNameChange,
    authPhoneChange,
    authEmailChange,
    authPasswordChange,
    authCreateUser,
})(Register);
