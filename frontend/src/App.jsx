import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { getAppConfig } from './config/appConfig';
import Layout from './components/Layout';
import Home from './pages/Home';
import ItemList from './pages/ItemList';
import ItemDetail from './pages/ItemDetail';
import CreateItem from './pages/CreateItem';
import SearchResults from './pages/SearchResults';
import Users from './pages/Users';
import Profile from './pages/Profile';
import AuthorProfile from './pages/AuthorProfile';
import NotFound from './pages/NotFound';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  const appConfig = getAppConfig();

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route index element={<Home />} />
            <Route path="items" element={<ItemList />} />
            <Route path="items/:id" element={<ItemDetail />} />
            <Route path="create" element={<CreateItem />} />
            <Route path="search" element={<SearchResults />} />
            <Route path="users" element={<Users />} />
            <Route path="profile" element={<Profile />} />
            <Route path="author/:authorId" element={<AuthorProfile />} />
            <Route path="category/:category" element={<ItemList />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;

