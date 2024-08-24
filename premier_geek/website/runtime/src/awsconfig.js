export const config = {
    Auth: {
        Cognito: {
            userPoolId: process.env.REACT_APP_USER_POOL_ID,
            userPoolClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID,
        }
    }
}
