VALID_CATEGORIES = [
    "Social Impact",
    "AMP (Advertising, Media, Publishing)",
    "Health and Beauty",
    "Manufacturing",
    "Food and Beverage",
    "AFA (Apparel, Footwear, Accessories)",
    "General Business",
    "Restaurant and Hospitality",
    "Retail",
    "Software",
    "Wholesale Distribution"
    "Campus Stores",    
    "Services",     
]

VERTICAL_SUMMARIES = {
"Social Impact": {
    "vertical_summary": """The Nonprofit vertical encompasses organizations whose primary mission is to serve the public interest, rather than generate profit.  They operate across diverse micro-verticals, including human services, faith communities, education, and arts & culture.  Nonprofits rely heavily on donations, grants, and fundraising activities to support their operations and achieve their missions. They are subject to specific accounting standards and regulatory requirements, and often leverage technology to manage donations, track program effectiveness, and engage with constituents.""",
    "qualifying_criteria": """
- Mission-Driven: The organization's primary purpose is to serve a public or community benefit, not to generate profit for owners or shareholders.
- Funding Sources: The organization relies on donations, grants, fundraising events, and other non-commercial revenue streams to fund its operations.
- Tax-Exempt Status: The organization holds tax-exempt status under section 501(c) of the Internal Revenue Code or a similar designation in its jurisdiction.
- Public Accountability: The organization is accountable to the public and often required to disclose financial and program information through filings like Form 990.
- Program Focus: The organization operates programs or provides services aligned with its mission, such as providing social services, promoting education, or advancing a specific cause.
- Donor Management: The organization actively engages in donor cultivation, solicitation, and stewardship activities to build relationships and secure funding.
- Volunteer Involvement: Many nonprofits rely on volunteers to support their programs and operations.
- Technology Utilization: The organization may utilize technology solutions like CRM, fundraising platforms, and program management software to streamline operations and enhance impact.
""",
    "keywords": {
      "tier1": ["nonprofit organization", "charity", "foundation", "NGO", "501c3"],
      "tier2": ["donation", "grant", "fundraising", "philanthropy", "social impact"],
      "tier3": ["volunteer", "community service", "public benefit", "mission-driven"],
      "negative": ["for-profit", "publicly traded", "shareholder", "dividend"]
    }  
  },
"AMP (Advertising, Media, Publishing)": {
    "vertical_summary": """The Advertising Agency vertical encompasses businesses that plan, create, and manage advertising campaigns for their clients.  They can specialize in various areas such as creative design, media buying, digital marketing, or offer full-service solutions. Agencies work with clients across diverse industries, helping them promote their brands and achieve their marketing objectives.  Revenue models often include fees, commissions, and performance-based incentives.""",
    "qualifying_criteria": """
- Client Services: The business provides advertising and marketing services to clients, acting as an external partner to manage their advertising needs.
- Campaign Management: The business plans, develops, and executes advertising campaigns across various channels (digital, print, broadcast, etc.).  This includes defining target audiences, setting campaign goals, and managing budgets.
- Creative Services: Many agencies offer creative services such as graphic design, copywriting, and video production to develop advertising materials.  Some specialize exclusively in creative work.
- Media Buying and Planning:  Agencies often handle media buying and planning, selecting appropriate media channels (websites, publications, TV/Radio) and negotiating ad placements for their clients.
- Digital Marketing:  A growing number of agencies specialize in digital marketing services like search engine optimization (SEO), social media marketing, and pay-per-click (PPC) advertising.
- Performance Tracking and Reporting: Agencies monitor campaign performance, track key metrics, and provide regular reports to clients on the effectiveness of their advertising efforts.
- Revenue Models:  Agencies typically generate revenue through fees for their services, commissions on media buys, or performance-based incentives tied to campaign results.
- Technology Utilization: Agencies leverage various technology platforms and tools for project management, campaign tracking, ad serving, and client communication.
""",
    "keywords": {
      "tier1": ["advertising agency", "marketing agency", "media buying agency", "creative agency", "digital agency"],
      "tier2": ["advertising campaign", "media planning", "brand management", "marketing strategy", "digital marketing"],
      "tier3": ["SEO", "social media marketing", "PPC", "content marketing", "email marketing"],
      "negative": ["media company", "publisher", "broadcaster", "manufacturer"]
    }
  },
"Health and Beauty": {
        "vertical_summary": """
The Health and Beauty vertical encompasses businesses involved in the manufacturing, distribution, and retail of products related to personal care, cosmetics, and wellness. These businesses range from small startups focusing on niche products to large multinational corporations with diverse product lines. They cater to a broad customer base concerned with enhancing their appearance, health, and well-being. Products commonly offered include cosmetics, skincare, hair care, supplements, fragrances, and personal care items.
""",
        "qualifying_criteria": """
- Products Offered: The business primarily offers products falling under the categories of cosmetics, skincare, hair care, fragrances, personal care (e.g., bath products, oral care), or wellness supplements.
- Target Market: The business primarily targets consumers interested in personal care, beauty enhancement, or health and wellness.
- Business Model: The business operates as a manufacturer, wholesaler, or retailer of health and beauty products. This may include direct-to-consumer sales (e.g., through e-commerce or brick-and-mortar stores), wholesale distribution to other retailers, or a combination of both.
- Regulatory Compliance: The business must comply with relevant regulations and safety standards for the manufacturing, labeling, and distribution of health and beauty products (e.g., FDA regulations in the US).
- Supply Chain Management: The business typically manages a complex supply chain involving raw materials sourcing, manufacturing or product formulation, packaging, and distribution to various sales channels.
- Technology Utilization: The business often utilizes technologies such as e-commerce platforms, inventory management systems, and customer relationship management (CRM) software to streamline operations and enhance customer experience.
- Marketing and Branding: The business often invests heavily in marketing and branding activities to build brand awareness, promote products, and engage with target customers. This may involve social media marketing, influencer collaborations, and traditional advertising.
- Scale of Operations: The business can range in size from small startups with limited product lines to large enterprises with global operations and diverse product portfolios.
""",
        "keywords": {
            "tier1": ["cosmetics manufacturer", "skincare line", "beauty products", "health supplements"],
            "tier2": ["wellness solutions", "personal care items", "natural remedies", "beauty treatments"],
            "tier3": ["skin", "hair", "nail", "spa", "salon", "wellness"],
            "negative": ["restaurant", "software development", "industrial manufacturing"]
        }
    },
"Manufacturing": {
        "vertical_summary": """
The Manufacturing vertical encompasses businesses that transform raw materials into finished goods through various processes, including engineering, design, production, and assembly. These businesses can range from small job shops producing custom products to large-scale enterprises manufacturing standardized goods for mass markets. Manufacturing companies prioritize production efficiency, inventory control, cost management, and often utilize specialized software and equipment to optimize their operations and ensure product quality. Their revenue streams primarily stem from the sale of manufactured goods, either directly to consumers (B2C) or through distribution channels (B2B).
""",
        "qualifying_criteria": """
- Production processes: The business engages in activities that transform raw materials into finished goods. These activities may include cutting, shaping, assembling, or processing materials using specialized machinery and equipment.
- Bill of Materials (BOM): The business utilizes BOMs to define the components, quantities, and assembly instructions for each product they manufacture.
- Inventory management: The business manages raw materials, work-in-progress (WIP) inventory, and finished goods inventory. They may utilize inventory management systems to track stock levels, optimize production schedules, and minimize waste.
- Production planning and scheduling: The business employs production planning and scheduling techniques to ensure efficient resource allocation, optimize production workflows, and meet customer demand. They may utilize manufacturing resource planning (MRP) or enterprise resource planning (ERP) systems to support these processes.
- Quality control: The business implements quality control measures throughout the manufacturing process to ensure product quality and compliance with industry standards. This may involve inspections, testing, and adherence to quality management systems (e.g., ISO 9001).
- Equipment and technology: The business utilizes specialized machinery, equipment, and technology to support their manufacturing processes. This may include computer numerical control (CNC) machines, robotics, automation systems, or specialized software for design, production, and quality control.
- Sales channels: The business sells its manufactured goods either directly to consumers (B2C) through retail stores or online channels, or through distribution networks (B2B) to wholesalers, retailers, or other businesses.
- Compliance and regulations: Depending on the industry and specific products manufactured, the business may be subject to industry-specific regulations and compliance requirements related to product safety, environmental protection, or labor standards.
""",
        "keywords": {
            "tier1": ["production line", "assembly plant", "manufacturing process", "industrial fabrication"],
            "tier2": ["quality control", "supply chain management", "raw material processing", "product engineering"],
            "tier3": ["factory", "machine", "assembly", "production", "fabricate"],
            "negative": ["software development", "consulting service", "retail store"]
        }
    },
"Food and Beverage": {
        "vertical_summary": """
The Food & Beverage industry encompasses businesses involved in the production, distribution, and sale of food and beverage products. These businesses cater to the daily needs of consumers, offering products that require frequent replenishment. This industry can be broadly categorized into manufacturers and distributors, with manufacturers ranging from small-scale producers to large-scale operations, and distributors specializing in various product categories and target markets.
""",
        "qualifying_criteria": """
- Products Offered: The primary products offered fall within the food and beverage categories, including but not limited to packaged foods, beverages (alcoholic and non-alcoholic), snacks, and tobacco products.
- Target Market: The target market is generally the general public or specific consumer segments (e.g., health-conscious consumers, specific dietary needs). Businesses may also target other businesses, such as restaurants, retailers, or institutions.
- Business Model: Companies in this vertical operate under various models, including manufacturing (in-house or outsourced), distribution (wholesale, retail), or a combination of both.
- Regulatory Environment: Businesses in the Food & Beverage industry are subject to stringent regulations concerning food safety, labeling, and quality control, including compliance with FDA regulations (in the US) or equivalent bodies in other regions.
- Technology Used: Companies often utilize specialized equipment for processing, packaging, and storing food and beverage products. This includes industrial kitchens, bottling lines, refrigeration systems, and inventory management software.
- Supply Chain Complexity: Operations often involve complex supply chains, encompassing sourcing raw materials, manufacturing, warehousing, and distribution to various sales channels.
- Inventory Management: Efficient inventory management is crucial due to product perishability and fluctuating demand. Real-time inventory tracking and forecasting are often critical for success.
- Sales Channels: Products are sold through various channels, including direct-to-consumer (e-commerce, retail stores), wholesale distribution to businesses, or a combination of both.
""",
        "keywords": {
            "tier1": ["food production", "beverage manufacturing", "culinary products", "drink distribution"],
            "tier2": ["ingredient supplier", "food packaging", "flavor development", "nutritional formulation"],
            "tier3": ["taste", "recipe", "nutrient", "organic", "dietary"],
            "negative": ["clothing", "software", "automotive"]
        }
    },
"AFA (Apparel, Footwear, Accessories)": {
        "vertical_summary": """
The Apparel, Footwear & Accessories (AFA) industry encompasses businesses involved in the design, manufacturing, distribution, and retail of clothing, shoes, and accessories. This industry caters to a diverse customer base, ranging from individual consumers to businesses, and includes various business models, from digitally native brands to traditional brick-and-mortar retailers and wholesalers. AFA businesses prioritize inventory visibility, production management, order fulfillment, customer experience, and omnichannel strategies to thrive in a competitive market.
""",
        "qualifying_criteria": """
- Products Offered: The business primarily sells apparel, footwear, or accessories. This can include clothing items like shirts, pants, dresses, outerwear, shoes of various types, and accessories such as jewelry, bags, belts, hats, etc.
- Target Market: The business caters to either individual consumers (B2C) or businesses involved in the resale of AFA products (B2B), or both.
- Sales Channels: The business utilizes various sales channels, such as online stores (e-commerce), physical retail stores, wholesale distribution, or a combination thereof (omnichannel).
- Inventory Management: The business places significant emphasis on managing inventory across multiple locations (warehouses, stores) and utilizes inventory management software or systems.
- Supply Chain Focus: The business actively manages its supply chain, including sourcing raw materials, manufacturing or outsourcing production, and potentially managing logistics and fulfillment.
- Customer Experience: The business prioritizes providing a positive customer experience, including aspects such as personalized recommendations, online and in-store returns, and customer service.
- Seasonality and Trends: The business operations are often influenced by seasonal trends and fashion cycles, requiring strategies for managing fluctuating demand and new product introductions.
- Technology Use: The business frequently utilizes technology solutions for various aspects of operations, such as e-commerce platforms, point-of-sale systems, inventory management software, and customer relationship management (CRM) tools.
""",
        "keywords": {
            "tier1": ["apparel manufacturer", "footwear design", "accessory production", "fashion house"],
            "tier2": ["clothing line", "shoe collection", "handbag series", "garment industry", "textile production"],
            "tier3": ["style", "fashion", "wear", "outfit", "trend", "design", "fabric"],
            "negative": ["food", "software", "restaurant", "technology"]
        }
    },
"General Business": {
        "vertical_summary": """
The General Business vertical is a broad category encompassing businesses that don't fit neatly into traditional industry verticals. These companies offer a diverse range of products and services, serving both individual consumers and other businesses. They often share common needs like streamlined financials, efficient operations, and adaptable solutions to support their varied business models and growth strategies.
""",
        "qualifying_criteria": """
- Diverse Products/Services: The company offers a range of products or services that may not be easily categorized into a specific industry vertical.
- Varied Customer Base: The company may serve a mix of individual consumers (B2C) and other businesses (B2B).
- Adaptable Business Model: The company may operate under various business models, including direct sales, wholesale, subscription services, franchises, or a combination of these.
- Technology Agnostic: While technology utilization is important, the company's core business does not inherently rely on a specific technology or software platform.
- Scalability Challenges: The company may experience rapid growth or expansion, requiring adaptable systems and processes to manage increased complexity.
- Integration Needs: The company often uses a variety of software systems for different business functions and needs to ensure smooth data flow and integration between them.
- Financial Focus: Strong financial management is crucial for these businesses, as they often have diverse revenue streams and complex financial reporting requirements.
- Operational Efficiency: Streamlined operations and efficient processes are essential to manage costs and maintain profitability across a diverse range of products or services.
""",
        "keywords": {
            "tier1": [],
            "tier2": [],
            "tier3": [],
            "negative": []
        }
    },
"Restaurant and Hospitality": {
        "vertical_summary": """
The Restaurant and Hospitality vertical encompasses businesses that provide food service, lodging, and related experiences to customers. This sector focuses on creating satisfying culinary experiences and comfortable stays, blending elements of gastronomy, accommodation, leisure, and customer service. The clientele includes local diners, tourists, business travelers, and event attendees seeking anything from a quick meal to an extended luxury stay.
""",
    "qualifying_criteria": """
- Offers food and/or accommodation services: Prepares and serves meals or provides lodging for short or extended stays.
- Prioritizes customer experience: Creates positive, memorable experiences through high-quality service, ambiance, and amenities.
- Employs specialized staff: Has teams dedicated to culinary arts, guest services, housekeeping, and facility management.
- Complies with industry regulations: Adheres to food safety, sanitation, and hospitality-specific legal requirements.
- Utilizes management systems: Employs specialized software for operations, such as point-of-sale systems or property management tools.
- Manages complex logistics: Handles inventory, supply chain, reservations, and facility maintenance.
- Provides auxiliary services: May offer amenities like event hosting, catering, room service, or recreational activities.
- Adapts to market demands: Responds to seasonal fluctuations, trends, and diverse customer needs.
- Generates varied revenue streams: Income sources include food and beverage sales, room rentals, and additional guest services.
- Scales across various sizes: Ranges from small, independent establishments to large chains and resorts.
- Implements loyalty programs: Often uses reward systems to encourage repeat business.
- Focuses on ambiance and setting: Creates environments that enhance dining or lodging experiences.
- Emphasizes staff training: Invests in employee development to maintain service standards.
- Manages online presence: Maintains digital platforms for marketing, bookings, and customer feedback.

This combined criteria set applies to a spectrum of businesses in the sector, from standalone restaurants to full-service hotels and integrated resorts, reflecting the interconnected nature of food service and hospitality.
""",
        "keywords": {
            "tier1": ["restaurant chain", "hotel services", "catering business", "hospitality management"],
            "tier2": ["food service", "guest accommodations", "dining experience", "event hosting"],
            "tier3": ["menu", "reservation", "guest", "chef", "cuisine"],
            "negative": ["software company", "manufacturing plant", "retail products"]
        }
    },
"Retail": {
        "vertical_summary": """
The Retail vertical encompasses businesses that sell consumer goods or services to individual customers through various distribution channels, aiming to earn a profit. These businesses typically fulfill smaller orders from a large number of end-users, as opposed to wholesalers or B2B companies. Retailers can operate through physical stores, online platforms, catalogs, or a combination of these channels in a multi-channel strategy. Key characteristics of this vertical include inventory management, customer relationship management, and a focus on delivering a positive customer experience.
""",
        "qualifying_criteria": """
- Primary Business Activity: Sells goods or services directly to individual consumers for personal use (B2C).
- Distribution Channels: Operates through one or more retail channels, such as physical stores, e-commerce websites, catalogs, or marketplaces.
- Inventory Management: Holds and manages inventory of goods intended for sale to consumers.
- Customer Focus: Prioritizes customer experience and satisfaction through aspects like customer service, loyalty programs, and personalized marketing.
- Revenue Model: Primarily generates revenue from the sale of goods or services at a markup over cost.
- Regulatory Environment: Complies with relevant retail regulations, such as sales tax laws and consumer protection laws.
- Technology: Utilizes point-of-sale (POS) systems, inventory management software, e-commerce platforms, and customer relationship management (CRM) systems.
- Scale: Can range from small, independent retailers to large, multinational chains.
""",
        "keywords": {
            "tier1": ["retail chain", "e-commerce platform", "store operations", "consumer goods sales"],
            "tier2": ["point of sale", "inventory management", "customer service", "retail marketing"],
            "tier3": ["shop", "store", "buy", "sell", "customer", "price"],
            "negative": ["software development", "manufacturing plant", "wholesale only"]
        }
    },
"Software": {
        "vertical_summary": """
The software industry encompasses businesses that develop, sell, and maintain software products and services. These businesses are characterized by a customer-centric approach, a focus on recurring revenue models (such as subscriptions), and a fast-growing, often globally expanding nature. They commonly offer a range of software solutions, including cloud-based applications (SaaS), enterprise resource planning (ERP) systems, and customer relationship management (CRM) tools, targeting diverse customer bases from individuals to large enterprises.
""",
        "qualifying_criteria": """
- Primary Product/Service: Offers software products or services (e.g., SaaS, on-premise software, mobile apps, cloud infrastructure).
- Revenue Model: Primarily generates revenue through software licenses, subscriptions, or usage-based fees.
- Target Market: Sells software to businesses (B2B) or individual consumers (B2C).
- Business Model: Operates on a recurring revenue model with a focus on customer retention and expansion (e.g., subscriptions, software updates).
- Technology/Equipment: Employs software development tools, programming languages, and cloud computing platforms.
- Regulatory Environment: May be subject to data privacy regulations (e.g., GDPR, CCPA), intellectual property laws, and industry-specific compliance standards.
- Sales Model: Utilizes sales-assisted approaches for enterprise software or self-service platforms for consumer software.
- Growth Strategy: Often prioritizes rapid growth through product innovation, international expansion, and potential acquisitions.
""",
        "keywords": {
            "tier1": ["software development", "SaaS platform", "cloud computing", "enterprise solutions"],
            "tier2": ["application programming", "software engineering", "tech startup", "IT services"],
            "tier3": ["code", "programming", "algorithm", "database", "API"],
            "negative": ["hardware manufacturing", "retail store", "restaurant"]
        }
    },
"Wholesale Distribution": {
        "vertical_summary": """
Wholesale Distribution is a business vertical focused on the procurement, storage, and distribution of goods to other businesses, typically retailers or other intermediaries, rather than directly to consumers. These businesses act as a crucial link in the supply chain, connecting manufacturers with retailers or businesses that need their products for resale or use in their operations. Wholesale distributors handle a wide range of products, manage inventory, and often provide logistics and fulfillment services to their customers. Their target market is typically businesses that require large quantities of goods for resale or use in their own production processes.
""",
        "qualifying_criteria": """
- Primary Business Activity: Sells goods in bulk to other businesses (B2B) rather than directly to consumers (B2C).
- Customer Base: Primarily comprised of retailers, other wholesalers, or businesses that use the products in their operations.
- Revenue Model: Revenue is primarily generated through the markup on goods sold, with profits derived from the difference between the purchase price from manufacturers and the selling price to customers.
- Inventory Management: Possesses significant warehouse space and utilizes inventory management systems to track stock levels, manage orders, and optimize logistics.
- Logistics and Fulfillment: Often provides services like order processing, shipping, and handling of returns for their customers.
- Product Variety: May specialize in a specific product category or carry a diverse range of products across multiple industries.
- Technology Utilization: Employs software solutions for inventory management, order processing, accounting, and potentially CRM to manage customer relationships.
- Regulatory Compliance: May be subject to industry-specific regulations related to the storage, handling, and transportation of goods, depending on the product categories handled.
""",
        "keywords": {
            "tier1": ["wholesale supplier", "distribution network", "bulk sales", "B2B distribution"],
            "tier2": ["inventory management", "logistics operations", "supply chain solutions", "warehouse management"],
            "tier3": ["bulk", "distribute", "supplier", "warehouse", "shipment"],
            "negative": ["direct to consumer", "software development", "restaurant"]
        }
    },
"Campus": {
    "vertical_summary": """The Campus vertical focuses on college bookstores and auxiliary services supporting educational institutions in North America. College bookstores handle general merchandise, technology, and course materials, focusing on student experience. Auxiliary services encompass crucial aspects of student life, like dining, housing, and activities, contributing significantly to the overall college experience.""",
    "qualifying_criteria": """
- Target Market: The business specifically serves colleges and universities, including students, faculty, and staff.  
- Products/Services: The business offers products or services tailored to the campus environment. This might include textbooks, general merchandise, technology products, dining services, student housing, event management, or other auxiliary services.
- Revenue Streams:  Revenue comes primarily from student spending, tuition fees (for auxiliary services), or designated university budgets.  For bookstores, revenue breakdown often involves a mix of textbooks, course materials, general merchandise, and technology products.
- Technology Integration: Integration with Student Information Systems (SIS) and other campus systems is often a key requirement for managing student data, course enrollment, and financial transactions.
- Point of Sale (POS) System:  Campus bookstores and dining services require specialized POS systems capable of handling student IDs, meal plans, and other campus-specific transactions.
- Financial Management:  Financial operations may involve managing multiple departments or cost centers, tracking departmental budgets, and consolidating financial reports across various auxiliary services.
- Ecommerce/Omnichannel: Many campus bookstores now offer online ordering and fulfillment options, requiring ecommerce integration and omnichannel capabilities.
- Compliance:  Businesses operating on campus may need to comply with specific regulations or reporting requirements set by the educational institution or governing bodies.
""",
    "keywords": {
      "tier1": ["college bookstore", "university bookstore", "campus store", "auxiliary services", "student dining"],
      "tier2": ["textbooks", "course materials", "student housing", "campus events", "meal plans"],
      "tier3": ["higher education", "student life", "campus", "university", "college"],
      "negative": ["K-12", "public school", "online education", "corporate training"]
    }
  },
  "Services": {
    "vertical_summary": """The Financial Services vertical encompasses businesses that manage money and assets, offering services related to investment, lending, and financial management. This includes a broad range of sub-industries, such as credit unions, banks, credit card companies, insurance firms, investment funds, mortgage companies, and private equity firms. These organizations face challenges like fluctuating interest rates, market volatility, regulatory changes, and increasing competition.""",
    "qualifying_criteria": """
- Regulated Industry: The business operates in a heavily regulated environment, subject to specific compliance requirements and oversight by regulatory bodies (e.g., SEC, FDIC, state insurance commissions).
- Financial Products/Services:  The business offers financial products or services, such as loans, investments, insurance policies, or financial management solutions.
- Risk Management:  Risk management is a core aspect of the business, involving assessing and mitigating financial risks, including credit risk, market risk, and operational risk.
- Capital Management: The business actively manages its capital structure and allocation to ensure financial stability and meet regulatory capital requirements.
- Financial Reporting:  Accurate and timely financial reporting is crucial, often necessitating compliance with specific accounting standards (e.g., GAAP, IFRS, Statutory Accounting Principles).
- Customer Due Diligence (CDD) and Know Your Customer (KYC):  Financial services firms typically have robust CDD and KYC processes to verify customer identities and comply with anti-money laundering (AML) regulations.
- Technology Adoption: The business often relies heavily on technology for financial modeling, risk assessment, transaction processing, customer relationship management (CRM), and regulatory reporting.
- Security Compliance:  Strong security measures are essential to protect sensitive financial data and comply with data privacy regulations.
""",
    "keywords": {
      "tier1": ["bank", "credit union", "insurance company", "investment fund", "mortgage lender", "private equity firm"],
      "tier2": ["loan", "investment", "insurance policy", "financial advisor", "asset management", "wealth management"],
      "tier3": ["finance", "banking", "investment", "insurance", "fintech"],
      "negative": ["retail bank", "commercial bank", "investment bank"] 
    }
  },
}