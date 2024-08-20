import Template from "./template/Template.js";
import ProductDetail from "./products/detail/ProductDetail.js";
import { Switch, Route, BrowserRouter } from "react-router-dom";
import Landing from "./landing/Landing.js";
import ProductList from "./products/ProductList.js";
import Login from "./profile_info/Login.js";
import Profile from "./profile_info/Profile.js";
import Header from "./template/Header.js";
import useToken from "./profile_info/UseToken.js";

function App() {
  const { token, removeToken, setToken } = useToken();
  // Breaks down the 3 components returned from useToken.js. We need functionality to remove and set token.

  return (
    <BrowserRouter>
      <div className="App">
        <Header token={removeToken} />
        {!token && token !== "" && token !== undefined ? (
          <Login setToken={setToken} />
          // Ternary operator -- if no token then anytime website first opened, defaults to log-in page. Otherwise can access below pages.
        ) : (
          <Template>
            <Switch>
              <Route path="/products" exact>
                <ProductList />
              </Route>
              <Route path="/products/:slug">
                <ProductDetail />
              </Route>
              <Route path="/profile" exact>
                <Profile token={token} setToken={setToken} />
              </Route>
              <Route path="/" exact>
                <Landing />
              </Route>
            </Switch>
          </Template>
        )}
      </div>
    </BrowserRouter>
  );
}

export default App;
