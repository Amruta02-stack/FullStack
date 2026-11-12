import { useState,useEffect } from "react";

export default function BrowsePage(){
    const[products,setProducts]=useState([]);
    const[page,setPage]=useState(1);

    useEffect(()=>{
            async function loadProducts() {
                const skip = (page - 1)*10
                const res = await fetch(`https://dummyjson.com/products?limit=10&skip=${skip}`)   
                const data = await res.json();
    
                setProducts(data.products);
                
            }
            loadProducts();
        },[page]);
    
    return(
        <>
        <p>Loaded {products.length} Products.</p>
        <button disabled={page === 1} onClick = {()=>setPage(page - 1)}>Previous</button>
        <span>Page: {page}</span>
        <button disabled={products.length === 0}onClick ={()=>setPage(page + 1)}>Next</button>
        
             <ol>
                {products.map((p)=>(
                    
                    
                    <li key = {p.id}>
                        <img src={p.thumbnail}></img>
                        <h3>Title :{p.title}</h3>
                        <h3>Price: {p.price}</h3>
                        <h3>Rating :{p.rating}</h3>
                        <h3>Category :{p.category}</h3>
                        <p><b>Number of reviews : {p.reviews.length}</b></p>
                    </li>
                ))}            
             </ol>
             </>
    )
}
