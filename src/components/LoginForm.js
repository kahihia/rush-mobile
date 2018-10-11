import React from 'react';
import { 
    View, 
    Text, 
    Image, 
    TouchableOpacity, 
    Dimensions,
    LayoutAnimation,
    Platform,
    UIManager,
} from 'react-native';
import { connect } from 'react-redux';
import { Divider } from 'react-native-elements';
import { 
    InputIcon, 
    Button, 
    TextLine, 
    Spinner,
    AuthBg,
} from './common';
import { YELLOW, LIGHT_RED } from './common/colors';
import { 
    authEmailChange,
    authPasswordChange,
    authLogin,
    authToRegister,
    authForgetPassword,
} from '../actions';

class LoginForm extends React.Component {
    state = {
        secureTextEntry: true,
    }

    componentWillMount() {
        const { appName } = styles;
        const { width } = Dimensions.get('window');

        // Responsive Condition
        if (width > 375) {
            this.setState({ 
                ...this.state, 
                logoSize: { width: 132, height: 185 }, 
                headerName: appName  
            });
        } else if (width > 320) {
            this.setState({ 
                ...this.state, 
                logoSize: { width: 105.6, height: 148 }, 
                headerName: { ...appName, fontSize: 32 } 
            });
        } else {
            this.setState({ 
                ...this.state, 
                logoSize: { width: 88, height: 123.33 }, 
                headerName: { ...appName, fontSize: 27 } 
            });
        }
    }

    componentWillUpdate() {
        LayoutAnimation.easeInEaseOut();
    }

    onEmailChange(text) {
        this.props.authEmailChange(text);
    }

    onPasswordChange(text) {
        this.props.authPasswordChange(text);
    }

    onUserLogin() {
        const { email, password } = this.props;
        this.props.authLogin(email, password);
    }

    renderLoginButton() {
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
                    color={YELLOW}
                    onPress={this.onUserLogin.bind(this)}
                >
                    เข้าสู่ระบบ
                </Button>
                <TextLine title='or' />
                <Button 
                    color={LIGHT_RED}
                    onPress={() => this.props.authToRegister()}
                >
                    สมัครสมาชิก
                </Button>
            </View>
        );
    }

    render() {
        const { linkRight } = styles;
        const { secureTextEntry, logoSize, headerName } = this.state;
        if (Platform.OS === 'android') {
            // UIManager.setLayoutAnimationEnabledExperimental && 
            UIManager.setLayoutAnimationEnabledExperimental(true);
        }

        return (
            <AuthBg>

                {/* -- Logo Section -- */}
                <Image 
                    style={logoSize}
                    source={require('../images/r-logo.png')}
                />
                <View>
                    <Text style={headerName}>
                        R U S H
                    </Text>
                </View>

                <Divider style={{ height: 10 }} />
                
                {/* -- Input Section -- */}
                <InputIcon 
                    value={this.props.email}
                    placeholder='E-mail'
                    iconName='user'
                    type='evilicon'
                    onChangeText={this.onEmailChange.bind(this)}
                />
                <InputIcon
                    placeholder='Password'
                    iconName='lock'
                    type='evilicon'
                    secureTextEntry={secureTextEntry}
                    password
                    value={this.props.password}
                    onChangeText={this.onPasswordChange.bind(this)}
                    onPress={() => this.setState({ secureTextEntry: !secureTextEntry })}
                />
                <TouchableOpacity 
                    style={linkRight} 
                    onPress={() => this.props.authForgetPassword()}
                >
                    <Text style={{ color: 'white' }}>
                        forget password?
                    </Text>
                </TouchableOpacity>

                <Divider style={{ height: 20 }} />

                {/* -- Button Section -- */}
                {this.renderLoginButton()}

            </AuthBg>
        );
    }
}

const styles = {
    appName: {
        fontSize: 40,
        fontWeight: 'bold',
        color: 'white',
    },
    linkRight: {
        alignSelf: 'flex-end',
        marginHorizontal: '12%',
        marginTop: 5,
    },
    errorText: {
        alignSelf: 'center', 
        paddingBottom: 10, 
        color: LIGHT_RED, 
        shadowColor: 'black', 
        shadowOpacity: 0.5, 
        shadowOffset: { width: 1, height: 1 }, 
        textAlign: 'center',
    }
};

const mapStateToProps = ({ auth }) => {
    const { email, password, user, loading, error } = auth;
    return { email, password, user, loading, error };
};

export default connect(mapStateToProps, {
    authEmailChange,
    authPasswordChange,
    authLogin,
    authToRegister,
    authForgetPassword,
})(LoginForm);
