// Routes holds all the pages
// Route holds one page url
// link to prevent relode when we switch pages


import {Routes,Route,Link} from 'react-router'

import ProductsPage from "./pages/ProductsPage"
import BrowsePage from './pages/BrowsePage';
import ProductDetialPage from './pages/ProductDetailPage';

function App() {
 

  return (
    <>
    <nav>
      <Link to="/">All Products</Link> | <Link to="/browse">Browse</Link> 
    </nav>
    <Routes>
    <Route path ="/" element={<ProductsPage/>}/>
    <Route path ="/browse" element={<BrowsePage/>}/>
    <Route path ="/products/:id" element={<ProductDetialPage/>}/>
    <Route path ='*' element={<h1>404 Not Found</h1>}/>
    </Routes>
   </>
    );
}

export default App
