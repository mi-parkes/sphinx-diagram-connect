Web Application Component Diagram
=================================

.. plantuml::
   :alt: Web Application Component Diagram
   :width: 80%

   @startuml
   !include <C4/C4_Component>

   !pragma svginteractive true

   LAYOUT_WITH_LEGEND()

   Container_Boundary(web_application, "Web Application") {
      Component(product_catalog_controller, "Product Catalog Controller", "Spring MVC Controller", "Handles requests for Browse and searching products.")
      Component(product_repository, "Product Repository", "Spring Data JPA Repository", "Manages persistence of product data.")
      Component(shopping_cart_service, "Shopping Cart Service", "Spring Service", "Manages adding/removing items from the shopping cart.")
      Component(order_service, "Order Service", "Spring Service", "Handles order creation and processing.")
      Component(user_authentication_component, "User Authentication Component", "Spring Security", "Manages user login and authentication.")

      Rel(product_catalog_controller, product_repository, "Uses")
      Rel(product_catalog_controller, shopping_cart_service, "Uses")
      Rel(shopping_cart_service, product_repository, "Uses")
      Rel(order_service, shopping_cart_service, "Uses")
      Rel(user_authentication_component, product_catalog_controller, "Authenticates users for")
   }

   Container(database, "Database", "PostgreSQL", "Stores product information, customer details, and order data.")

   Rel(product_repository, database, "Reads from and Writes to")
   Rel(order_service, database, "Writes orders to")

   @enduml
