// useParams help handle the values(parameter) passed in the path

import { useParams } from "react-router";
import { useState,useEffect } from "react"; 
import { Link } from "react-router";

export default function ProductDetialPage(){
    const { id } = useParams();
    const[products,setProducts]=useState(null);
        
        useEffect(()=>{
            async function loadProducts() {
                const res = await fetch(`https://dummyjson.com/products/${id}`)   
                const data = await res.json();
    
                setProducts(data);
                
            }
            loadProducts();
        },[id]);

        if(!products) return <p>Loading.....</p>


    return(
    <>
                <Link to="/ ">Back to Home Page</Link>  

                <p>Title :{products.title}</p>
                <p>Price: {products.price}</p>
                <p>Rating :{products.rating}</p>
                <p>Category :{products.category}</p>
                <p><b>Number of reviews : {products.reviews.length}</b></p>
                <h3>Images</h3>
                 {products.images.map((image)=> (
                    <img key = {image} src= {image} width="150"></img>
                    ))}
                <h3>Reviwes</h3>
                {products.reviews.map((review)=>(
                    
                    <li>
                        {review.reviewerName} {review.rating}/5 : {review.comment}
                    </li>
                ))}
                    
                
    </>
)

}