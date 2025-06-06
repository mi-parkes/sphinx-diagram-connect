System Context Diagram
======================

.. plantuml::
   :alt: E-commerce System Context Diagram
   :width: 80%

   @startuml
   !include <C4/C4_Context>

   AddElementTag(clickable, $bgColor="lightgray", $fontColor="darkred", $borderColor="darkred", $shadowing="true", $shape="RoundedBoxShape()", $legendText="clickable")

   'LAYOUT_WITH_LEGEND()

   Person(customer, "Customer", "Uses the e-commerce website to browse and purchase products.")
   System(ecommerce_system, "E-commerce System", "Allows customers to browse, search, and purchase products online.",$tags="clickable") [[ ":ref:`container diagram`" ]]
   System(payment_gateway, "Payment Gateway", "Third-party system for processing payments.",\
   $link='":ref:`heading 1`"')
   System(delivery_service, "Delivery Service", "Third-party system for managing product deliveries.")

   Rel(customer, ecommerce_system, "Uses")
   Rel(ecommerce_system, payment_gateway, "Delegates payment processing to")
   Rel(ecommerce_system, delivery_service, "Notifies of orders for delivery")

   @enduml
