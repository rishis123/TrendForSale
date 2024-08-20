// We utiilize local storage -- store the JWT in the current browser, but allow across duplicates (like if open up another tab in website.)

import { useState } from 'react';

function useToken() {

    // Returns JWT if does exist and is not null
    function getToken() {
        const userToken = localStorage.getItem('token');
        return userToken && userToken
    }

    // Stores refreshed value -- useState hook indicates that if a value of either of those changes, to reload the React page.
    const [token, setToken] = useState(getToken());

    // Store token in local storage.
    function saveToken(userToken) {
        localStorage.setItem('token', userToken);
        setToken(userToken);
    };

    function removeToken() {
        localStorage.removeItem("token");
        setToken(null);
    }

    return {
        setToken: saveToken,
        // setToken variable stores saveToken function value, so call to setToken internally calls setToken
        token,
        removeToken
    }

}

export default useToken;