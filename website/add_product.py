from website import create_app, db
from website.models import Product
import os

app = create_app()

# Product data: (Price, Product_Type, Warranty, Model_ID, Image File Name, Description)
products_info = [
    (699.99, 'Laptop', 12, 1, "Inspiron 15.jpg",
     "Dell Inspiron 15 is a dependable all-rounder designed for daily productivity. Equipped with an Intel Core i5, 8GB RAM, "
     "and 256GB SSD, it delivers smooth multitasking performance. Its 15.6\" Full HD display provides vibrant visuals, and the full-size keyboard enhances typing comfort. "
     "Ideal for students and professionals who need a reliable, budget-friendly machine with strong battery life and solid connectivity options."),

    (1099.99, 'Laptop', 24, 2, "XPS 13.jpg",
     "Dell XPS 13 blends power with elegance. Featuring a sleek aluminum chassis, it houses an Intel Core i7, 16GB RAM, and 512GB SSD. "
     "The 13.3\" InfinityEdge display offers near-borderless viewing with rich colors. Great for professionals on the move, its portability, long battery life, "
     "and premium build make it perfect for presentations, video calls, and creative workflows."),

    (649.99, 'Laptop', 12, 3, "Pavilion 14.jpg",
     "HP Pavilion 14 offers a refined computing experience with an AMD Ryzen 5, 8GB RAM, and 512GB SSD. "
     "Its compact and stylish design makes it perfect for students or casual users. The 14\" FHD display, fast boot time, and responsive performance make everyday tasks—from streaming to document editing—efficient and enjoyable."),

    (899.99, 'Laptop', 24, 4, "Envy 13.jpg",
     "HP Envy 13 combines power, portability, and aesthetics. Equipped with an Intel Core i7, 16GB RAM, and 512GB SSD, it easily handles demanding apps. "
     "The 13.3\" FHD touchscreen is sharp and responsive, while the all-metal chassis adds a premium feel. Bang & Olufsen speakers, fingerprint sensor, and long battery life make it perfect for creatives and professionals alike."),

    (1299.99, 'Laptop', 36, 5, "ThinkPad X1 Carbon.jpg",
     "Lenovo ThinkPad X1 Carbon is a business-class ultrabook known for its military-grade durability and world-class keyboard. With an Intel Core i7, 16GB RAM, 1TB SSD, "
     "and a stunning 14\" UHD display, it's built for serious multitaskers. Features include a fingerprint reader, rapid charging, and a featherlight carbon fiber body—ideal for professionals who demand both power and portability."),

    (749.99, 'Laptop', 12, 6, "IdeaPad 5.jpg",
     "Lenovo IdeaPad 5 is a well-rounded laptop for home and office use. It features an AMD Ryzen 7 processor, 8GB RAM, and 512GB SSD, delivering excellent speed and responsiveness. "
     "Its 15.6\" Full HD display with narrow bezels ensures immersive viewing, while Dolby Audio speakers enhance entertainment. Perfect for those who need solid performance without breaking the bank."),

    (1199.99, 'Laptop', 24, 7, "MacBook Air M2.jpg",
     "The new MacBook Air with M2 chip sets a new standard for ultraportables. With 8GB RAM, 256GB SSD, and a brilliant 13.6\" Liquid Retina display, it offers impressive power in a thin, silent design. "
     "Ideal for students, developers, and everyday creatives, it supports seamless multitasking, powerful graphics, and over 18 hours of battery life—all in a fanless, ultra-light enclosure."),

    (1999.99, 'Laptop', 36, 8, "MacBook Pro 14.jpg",
     "Apple MacBook Pro 14 is engineered for performance-hungry professionals. Featuring the Apple M2 Pro chip, 16GB RAM, and 512GB SSD, it handles intensive tasks like video editing, 3D rendering, and music production with ease. "
     "Its 14.2\" Liquid Retina XDR display offers stunning brightness and contrast, while studio-quality microphones and powerful speakers enhance creative workflows. Built for professionals who demand excellence.")
]

with app.app_context():
    for price, product_type, warranty, model_id, image_name, description in products_info:
        image_path = os.path.join("website", "static", image_name)

        try:
            with open(image_path, "rb") as f:
                image_data = f.read()

            product = Product(
                Price=price,
                Product_Type=product_type,
                Warranty=warranty,
                Model_ID=model_id,
                Picture=image_data,
                Descriptions=description
            )

            db.session.add(product)
            print(f"Added product: {image_name}")

        except FileNotFoundError:
            print(f"Image file not found: {image_path}")

    db.session.commit()
    print("All products committed to the database.")
