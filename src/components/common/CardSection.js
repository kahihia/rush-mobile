import React from 'react';
import { View } from 'react-native';

const CardSection = ({ children }) => {
    return (
        <View style={{ marginHorizontal: '5%' }}>
            {children}
        </View>
    );
};

export { CardSection };
