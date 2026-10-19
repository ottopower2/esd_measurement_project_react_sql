import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles.css';
import Dashboard from './dashboard';
import Setting from './setting';

function Root() {
  const [route, setRoute] = React.useState(window.location.pathname);

  React.useEffect(() => {
    const handlePopState = () => {
      setRoute(window.location.pathname);
    };

    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const navigate = (path) => {
    if (window.location.pathname === path) {
      return;
    }

    window.history.pushState({}, '', path);
    setRoute(path);
  };

  const Component =
    route === '/dashboard' ? Dashboard : route === '/setting' ? Setting : App;

  return <Component navigate={navigate} />;
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>,
);
