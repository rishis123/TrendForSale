import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header>
      <nav className="navbar fixed-top navbar-expand-lg navbar-light bg-white border-bottom">
        <div className="container-fluid">
          {/* Profile link */}
          <Link className="navbar-brand" to="/profile">
            <FontAwesomeIcon
              icon={["fas", "user-alt"]}
              className="ms-1"
              size="lg"
            />
            <span className="ms-2 h5">Profile</span>
          </Link>

          {/* Shopping cart link */}
          <Link to="/cart" className="btn btn-outline-dark me-3 d-none d-lg-inline d-flex align-items-center">
            <FontAwesomeIcon icon={["fas", "shopping-cart"]} />
            <span className="ms-3 badge rounded-pill bg-dark">0</span>
          </Link>
        </div>
      </nav>
    </header>
  );
}

export default Header;