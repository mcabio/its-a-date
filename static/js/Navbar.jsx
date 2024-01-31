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
    <nav className="navbar navbar-expand-lg bg-dark border-bottom border-body" data-bs-theme="dark">

        <a className="navbar-brand">
        {isLoggedIn ? `Logged in as: ${username}` : null}
        </a>

    <button
      data-bs-theme="dark"
      className="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>

    <div className="collapse navbar-collapse" id="navbarSupportedContent" data-bs-theme="dark">
      <ul className="navbar-nav me-auto mb-2 mb-lg-2">
        <li className="nav-item active">
        <li className="nav-item dropdown">
          <a
          className="nav-link dropdown-toggle"
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
            <li><a className="dropdown-item" href="/dashboard">Calendar</a></li>
            <li><a className="dropdown-item" href="/my-availability">View availability</a></li>
            <li><a className="dropdown-item" href="/my-events">View my plans</a></li>
          </ul>
          </li>
        </li>
        <li className="nav-item">
            {isLoggedIn && userId !== null && (
            <a className="nav-link" href={`/edit-user/${userId}`}>
            Edit Preferences
            </a>
  )}
        </li>
      
      <form className="d-flex">
        <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
        <button className="btn btn-outline-success me-2" type="submit">Search</button>
      </form>

      
        </ul>
    </div>
  </nav>
  );
 }
  ReactDOM.render(<Navbar />, document.querySelector('#app'));