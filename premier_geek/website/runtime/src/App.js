import React, { useState } from 'react';
import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { config } from './awsconfig';
import { fetchAuthSession } from 'aws-amplify/auth';
import axios from 'axios';

Amplify.configure(config);

function App({ signOut, user }) {
  const [query, setQuery] = useState('');
  const [players, setPlayers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = () => {
    if (query.trim()) {
      callApi();
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  const callApi = async () => {
    setIsLoading(true);
    setError('');
    try {
      const session = await fetchAuthSession();
      const idToken = session.tokens.idToken.toString();

      const response = await axios.get(`${process.env.REACT_APP_API_URL}/players`, {
        params: { query },
        headers: {
          'Authorization': `Bearer ${idToken}`,
          'Content-Type': 'application/json'
        }
      });

      setPlayers(response.data);
      setHasSearched(true);
    } catch (error) {
      console.error('Error calling API:', error);
      setError(`The query is not related to PL squads. Try again.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-800 to-green-600 py-6 flex flex-col justify-center sm:py-12 relative">
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-full p-5 shadow-lg">
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-green-500"></div>
          </div>
        </div>
      )}
      <button
        onClick={signOut}
        className="absolute top-4 right-4 text-white text-sm bg-transparent hover:bg-white hover:bg-opacity-20 py-2 px-4 rounded transition duration-300 ease-in-out"
      >
        Sign out
      </button>
      <div className="relative py-3 sm:max-w-4xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-green-400 to-green-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-[#0d9655]" style={{ fontFamily: "'Barlow', sans-serif" }}>Premier Geek</h1>
              <p className="text-xl text-gray-600 mt-2">Your AI-powered Premier League squad explorer</p>
            </div>
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <div className="flex">
                  <input
                    type="text"
                    className="flex-1 px-4 py-2 border rounded-l-lg focus:ring-2 focus:ring-[#0d9655] focus:outline-none"
                    placeholder="Who plays for The Hammers?"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={isLoading}
                  />
                  <button
                    onClick={handleSearch}
                    className="px-4 py-2 bg-[#0d9655] text-white rounded-r-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-[#0d9655]"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Searching...' : 'Search'}
                  </button>
                </div>
                {error && <p className="text-red-500">{error}</p>}
              </div>
              <div className="py-8">
                {hasSearched ? (
                  players.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                      {players.map((player, index) => (
                        <div key={index} className="bg-white p-4 rounded-lg shadow-md flex flex-col h-full">
                          <img
                            src={player.image_path || 'https://via.placeholder.com/150'}
                            alt={`${player.first_name} ${player.surname}`}
                            className="w-full h-48 object-cover rounded-t-lg"
                          />
                          <div className="mt-4 flex flex-col flex-grow">
                            <h3 className="text-xl font-semibold mb-1">{`${player.first_name} ${player.surname}`}</h3>
                            <div className="flex-grow flex flex-col justify-start">
                              <p className="text-gray-600">{player.playing_position || 'n/a'}</p>
                              <p className="text-sm text-gray-500">{player.date_of_birth ? new Date(player.date_of_birth).toLocaleDateString() : 'n/a'}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center text-gray-500">No players found. Try a different query.</p>
                  )
                ) : (
                  <p className="text-center text-gray-500">Ask about any Premier League squad and click 'Search' to explore.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default withAuthenticator(App, {
  hideSignUp: true,
});
