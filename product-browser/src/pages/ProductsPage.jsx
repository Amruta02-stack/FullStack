import { useState,useEffect } from "react";
import { Link } from "react-router";

export default function ProductsPage(){
    const[products,setProducts]=useState([]);
    
    useEffect(()=>{
        async function loadProducts() {
            const res = await fetch("https://dummyjson.com/products")   
            const data = await res.json();

            setProducts(data.products);
            
        }
        loadProducts();
    },[]);

    return(
        <>
        <p>Loaded {products.length} Products.</p>
        <ol>
            {products.map((p)=>(

                
                <li key = {p.id}>
                    <img src={p.thumbnail}></img>
                    <h3>Title :{p.title}</h3>
                    <h3>Price: {p.price}</h3>
                    <h3>Rating :{p.rating}</h3>
                    <h3>Category :{p.category}</h3>
                    <p><b>Number of reviews : {p.reviews.length}</b></p>
                    <Link to = {`/products/${p.id}`}>Veiw Detail</Link>
                </li>
            ))}            
        </ol>

        </>
    );
}

// export default ProductPage;