# Microservice Frontend

A modern, responsive frontend application built with **Vite + React + Tailwind CSS** for the microservice architecture. This frontend supports multiple app configurations (blog, e-commerce, etc.) with dynamic metafields and seamless API integration through Kong Gateway.

## 🚀 Features

- **Multi-app Support**: Configure different app types (blog, e-commerce) with environment-based settings
- **Dynamic Metafields**: Custom fields per app type with form generation
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Modern UI**: Minimalist, clean interface with smooth transitions
- **API Integration**: Seamless integration with backend services through Kong Gateway
- **Authentication**: Login/register with JWT token management
- **Search**: Real-time search with autocomplete
- **Pagination**: Efficient pagination for large datasets
- **CRUD Operations**: Full create, read, update, delete functionality for items

## 🛠️ Tech Stack

- **Frontend Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **State Management**: React Hooks

## 📦 Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

## 🚀 Running the Application

### For Blog Application
```bash
npm run start:blog
```
This will:
- Load configuration from `.env.blog`
- Set app_id to "blog"
- Configure blog-specific metafields (excerpt, readTime, featured, publishedAt)
- Start development server on http://localhost:3000

### For E-commerce Application
```bash
npm run start:ecommerce
```
This will:
- Load configuration from `.env.ecommerce`
- Set app_id to "ecommerce"
- Configure e-commerce metafields (price, place, ratings, brand, availability, discount)
- Start development server on http://localhost:3000

### Development Mode (Default - Blog)
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## 🔧 Configuration

### Environment Files

The application uses environment-specific configuration files:

**`.env.blog`**:
```env
VITE_APP_CONFIG=blog
VITE_APP_ID=blog
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Blog Platform
VITE_META_FIELDS=["excerpt","readTime","featured","publishedAt"]
```

**`.env.ecommerce`**:
```env
VITE_APP_CONFIG=ecommerce
VITE_APP_ID=ecommerce
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=E-Commerce Platform
VITE_META_FIELDS=["price","place","ratings","brand","availability","discount"]
```

### API Configuration

The frontend connects to backend services through Kong API Gateway:
- **Base URL**: `http://localhost:8000`
- **Authentication**: `/auth/*`
- **Items**: `/items/*`
- **Search**: `/search/*`
- **Users**: `/users/*`

## 📱 Application Structure

```
src/
├── components/          # Reusable UI components
│   ├── Layout.jsx      # Main layout with navigation
│   ├── SearchBar.jsx   # Search functionality
│   ├── ItemCard.jsx    # Item display component
│   ├── Pagination.jsx  # Pagination component
│   └── MetaFieldForm.jsx # Dynamic form for metafields
├── pages/              # Page components
│   ├── Home.jsx        # Homepage with featured items
│   ├── ItemList.jsx    # Items listing with pagination
│   ├── ItemDetail.jsx  # Individual item view
│   ├── CreateItem.jsx  # Item creation form
│   ├── Login.jsx       # Login page
│   └── Register.jsx    # Registration page
├── services/           # API service layers
│   ├── api.js          # Axios configuration
│   ├── itemService.js  # Item-related API calls
│   ├── authService.js  # Authentication API calls
│   ├── searchService.js # Search API calls
│   └── userService.js  # User management API calls
├── config/             # Configuration files
│   └── appConfig.js    # App-specific configurations
└── utils/              # Utility functions
```

## 🎨 UI Components

### Responsive Design
- **Mobile-first**: Optimized for mobile devices
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Grid System**: CSS Grid and Flexbox for layouts

### Theme System
Each app configuration has its own theme:
- **Blog**: Blue color scheme
- **E-commerce**: Green color scheme
- **Customizable**: Easy to extend with new themes

## 📝 Features Overview

### 1. **Multi-App Configuration**
- Switch between different app types using environment files
- Each app has specific metafields and theme
- Dynamic form generation based on app configuration

### 2. **Item Management**
- **Create**: Rich form with metafields support
- **Read**: Detailed view with all information
- **Update**: Edit existing items (when authenticated)
- **Delete**: Remove items (when authenticated)

### 3. **Search & Discovery**
- **Real-time Search**: Search as you type
- **Categories**: Filter by categories
- **Authors**: View items by specific authors
- **Pagination**: Handle large datasets efficiently

### 4. **Authentication**
- **JWT Tokens**: Secure authentication
- **Auto-refresh**: Automatic token refresh
- **Protected Routes**: Authentication-based access
- **Google OAuth**: Ready for Google login integration

### 5. **Responsive UI**
- **Mobile Navigation**: Hamburger menu for mobile
- **Grid/List Views**: Toggle between view modes
- **Loading States**: Skeleton loading animations
- **Error Handling**: User-friendly error messages

## 🔒 Authentication Flow

1. **Login/Register**: User authenticates via `/auth` endpoints
2. **Token Storage**: JWT tokens stored in localStorage
3. **Auto-injection**: Tokens automatically added to API requests
4. **Auto-refresh**: Refresh tokens used for session management
5. **Route Protection**: Protected routes require authentication

## 🌐 API Integration

### Request Headers
All API requests include:
- `app_id`: Current app identifier (blog/ecommerce)
- `Authorization`: Bearer token (when authenticated)
- `Content-Type`: application/json

### Error Handling
- **401 Unauthorized**: Auto-redirect to login
- **Network Errors**: User-friendly error messages
- **Validation Errors**: Form-level error display

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Environment Variables for Production
Create appropriate environment files for your production setup:
- Update `VITE_API_BASE_URL` to your production API URL
- Configure other environment-specific variables

### Serve Static Files
The build output in `dist/` folder can be served by any static file server:
- Nginx
- Apache
- Netlify
- Vercel
- AWS S3 + CloudFront

## 🧪 Development

### Code Structure
- **Components**: Reusable UI components with props
- **Pages**: Route-level components
- **Services**: API abstraction layer
- **Hooks**: Custom React hooks for state management
- **Utils**: Helper functions and utilities

### Best Practices
- **Component Composition**: Small, focused components
- **State Management**: Local state with hooks
- **Error Boundaries**: Graceful error handling
- **Performance**: Lazy loading and code splitting
- **Accessibility**: ARIA labels and keyboard navigation

## 📋 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (default: blog) |
| `npm run start:blog` | Start with blog configuration |
| `npm run start:ecommerce` | Start with e-commerce configuration |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the microservice architecture and follows the same licensing terms as the parent project.

---

**Happy Coding! 🎉**
