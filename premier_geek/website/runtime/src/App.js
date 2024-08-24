import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { config } from './awsconfig';
import { fetchAuthSession } from 'aws-amplify/auth';
import axios from 'axios';


Amplify.configure(config);

function App({ signOut, user }) {
  const [apiResponse, setApiResponse] = useState('');

  const callApi = async () => {
    try {
      const session = await fetchAuthSession();
      const idToken = session.tokens.idToken.toString();
      const query = "Who plays for the hammers?";

      const response = await axios.get(`${process.env.REACT_APP_API_URL}/players`, {
        params: {
          query: query
        },
        headers: {
          'Authorization': `Bearer ${idToken}`,
          'Content-Type': 'application/json'
        }
      })

      setApiResponse(response.data.toString());
    } catch (error) {
      console.error('Error calling API:', error);
      setApiResponse('Error calling API: ' + error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
      <button onClick={signOut}>
          Sign out
        </button>
        <button onClick={callApi} style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginBottom: '10px'
        }}>
          Call API
        </button>
        {apiResponse && (
          <div style={{
            marginTop: '20px',
            padding: '10px',
            backgroundColor: '#f0f0f0',
            borderRadius: '5px',
            maxWidth: '80%',
            wordBreak: 'break-word'
          }}>
            <h3>API Response:</h3>
            <p>{apiResponse}</p>
          </div>
        )}on>
        <img src={logo} className="App-logo" alt="logo" />
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default withAuthenticator(App, {
  hideSignUp: true,
});
