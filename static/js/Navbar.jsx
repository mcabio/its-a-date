function Navbar() {
    const [isLoggedIn, setIsLoggedIn] = React.useState(false);
    const [username, setUsername] = React.useState('');
    const [userId, setUserId] = React.useState(null);
  
    React.useEffect(() => {
      fetch('/api/login-status')
        .then((response) => response.json())
        .then((result) => {
          setIsLoggedIn(result.logged_in);
          setUsername(result.username || '');
          setUserId(result.user_id || null);
        })
        .catch((error) => {
          console.error('Error fetching login status:', error);
        });
    }, []);
  
    if (!isLoggedIn) {
      // If the user is not logged in, return null or an empty div to hide the navbar
      return null;
    }
  
    return (
      <>
      <div style={{ marginTop: '56px' }}>
        <nav className="navbar navbar-expand-lg fixed-top" style={{ backgroundColor: '#433c5e', borderBottom: '1px solid #433c5e' }}>
          {/* Home Preferences link */}
          <ul className="navbar-nav">
                <li className="nav-item">
                <a className="nav-link" disabled>Logged in as: {username}</a>
                </li>
              </ul>

            {/* Home Preferences link */}
          {/* <ul className="navbar-nav">
                <li className="nav-item">
                <a className="nav-link" disabled>{isLoggedIn ? `Logged in as: ${username}` : null}</a>
                </li>
              </ul>
           */}
  
          <button
            data-bs-theme="dark"
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
  
          <div className="collapse navbar-collapse" id="navbarSupportedContent" data-bs-theme="dark">
            <ul className="navbar-nav me-auto mb-2 mb-lg-2">

              {/* Home Preferences link */}
              <ul className="navbar-nav mx-auto">
                <li className="nav-item">
                <a className="btn btn-outline-dark" href="/dashboard">Dashboard</a>
                </li>
              </ul>

              {/* My Planner dropdown */}
              <li className="nav-item dropdown">
                <a
                  className="btn btn-outline-dark"
                  href="#"
                  id="navbarDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  My Planner
                </a>
                <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
                  <li><a className="dropdown-item" href="/my-availability">View availability</a></li>
                  <li><a className="dropdown-item" href="/my-events">View my plans</a></li>
                </ul>
              </li>
             
  
              {/* Edit Preferences link */}
              <li className="nav-item">
                {isLoggedIn && userId !== null && (
                  <a className="btn btn-outline-dark" href={`/edit-user/${userId}`}>
                    Edit Preferences
                  </a>
                )}
              </li>
  
              {/* Search dropdown */}
              <li className="nav-item dropdown">
                <a className="btn btn-outline-dark"
                  href="#"
                  id="navbarDropdownSearch"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false">
                  Search
                </a>
                <ul className="dropdown-menu" aria-labelledby="navbarDropdownSearch">
                  <li><a className="dropdown-item" data-bs-toggle="modal" data-bs-target="#searchByDates">By Date Range</a></li>
                  <li><a className="dropdown-item" data-bs-toggle="modal" data-bs-target="#searchByTitle">By Event Name</a></li>
                </ul>
              </li>
            </ul>
  
            {/* Logout link */}
            <ul className="btn btn-outline-dark">
              <li className="nav-item">
                <a className="nav-link" href="/logout">Logout</a>
              </li>
            </ul>
          </div>
        </nav>
  
        {/* Search by Dates Modal */}
        <div className="modal fade" id="searchByDates" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h1 className="modal-title fs-5" id="staticBackdropLabel">Search Dates Between:</h1>
                <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div className="modal-body">
                <form action="/search-date-results" method="GET">
                  <div className="input-group">
                    <span className="input-group-text">Events between</span>
                    <input type="date" id="start_date" aria-label="Start range" className="form-control" name="start_date" required />
                    <input type="date" id="end_date" aria-label="End range" className="form-control" name="end_date" required />
                  </div>
                  <div className="modal-footer">
                    <button type="submit" className="btn btn-outline-danger">Search</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
  
        {/* Search by Title Modal */}
        <div className="modal fade" id="searchByTitle" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h1 className="modal-title fs-5" id="staticBackdropLabel">Search By Title</h1>
                <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div className="modal-body">
                <form action="/search-title-results" method="GET">
                  <div className="input-group">
                    <span className="input-group-text">Event keywords</span>
                    <input type="text" id="title" aria-label="Event Title" className="form-control" name="title" required />
                  </div>
                  <div className="modal-footer">
                    <button type="submit" className="btn btn-outline-danger">Search</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
        </div>
      </>
    );
  }
  
  ReactDOM.render(<Navbar />, document.querySelector('#app'));
  