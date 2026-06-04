import type { Product } from '../data/catalog';

type ProductCardProps = {
  product: Product;
};

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <article className="product-card">
      <span className="badge">{product.category}</span>
      <h3>{product.title}</h3>
      <p>{product.description}</p>
      <div className="product-footer">
        <div>
          <strong>{product.partNumber}</strong>
          <div className="compat">Compatible: {product.compatibility.join(', ')}</div>
        </div>
        <div className="price">{product.price}</div>
      </div>
    </article>
  );
}
