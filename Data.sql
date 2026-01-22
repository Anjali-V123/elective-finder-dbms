INSERT INTO Teacher VALUES
('TE000','Dr Tania'),
('TE001','Ms Asha'),
('TE002','Mr Ramod'),
('TE003','Mrs Ghosh'),
('TE004','Dr Nivedita'),
('TE005','Dr Nina'),
('TE006','Dr Prakash'),
('TE007','Dr Varun'),
('TE008','Dr Sneha'),
('TE009','Prof Kavya'),
('TE010','Dr Mahesh'),
('TE011','Prof Shreya');

INSERT INTO Elective (Course_ID, Course_Name, Syllabus, Class_Size, Elective_Number, Elective_Description, Semester) VALUES
('CS001','Advanced Algorithms',
 'Algorithm design, greedy algorithms, dynamic programming, divide and conquer, graph algorithms, shortest paths, minimum spanning tree, flows, NP-hard problems, approximation algorithms, complexity analysis, randomized algorithms, amortized analysis, data structures integration, string matching, suffix arrays, advanced sorting, hashing techniques, combinatorial optimization',
 '80','1','Advanced algorithmic techniques','5'),

('CS002','Data Analytics',
 'Data wrangling, pandas, numpy, exploratory data analysis, statistical inference, hypothesis testing, visualization with matplotlib and seaborn, feature engineering, dimensionality reduction, PCA, clustering, regression, classification, time-series analysis, evaluation metrics, data cleaning, EDA, SQL for analytics, dashboards, storytelling with data',
 '90','2','Data analysis and visualization','5'),

('CS003','Big Data',
 'Distributed storage, Hadoop HDFS, MapReduce, Spark core and Spark SQL, streaming with Spark Streaming, big data pipelines, batch processing, NoSQL databases (HBase, Cassandra), data ingestion, Kafka, scalability, cluster management, performance tuning, partitioning, distributed joins, serialization formats (Avro, Parquet), cloud big data services',
 '110','3','Large scale data processing','5'),

('CS004','Natural Language Processing',
 'NLP fundamentals, tokenization, stemming, lemmatization, POS tagging, named entity recognition, word embeddings (word2vec, GloVe), transformers, BERT, GPT, sequence models, attention mechanisms, machine translation, text classification, sentiment analysis, language modeling, text generation, evaluation metrics BLEU, ROUGE, subword tokenization',
 '30','4','Language understanding and generation','6'),

('CS005','Topics in Deep Learning',
 'Neural networks, CNNs, RNNs, LSTMs, Transformers, attention, transfer learning, optimization (adam, sgd), regularization (dropout, batchnorm), hyperparameter tuning, model interpretability, PyTorch implementation, TensorFlow basics, generative models (GANs, VAEs), computer vision applications, sequence modelling',
 '40','5','Deep learning concepts and projects','6'),

('CS006','Data Mining',
 'Association rules, frequent pattern mining (Apriori, FP-Growth), clustering (k-means, hierarchical, DBSCAN), classification (decision trees, random forest, SVM), outlier detection, evaluation measures precision recall F1, feature selection, ensemble methods, text mining, topic modeling (LDA), scalability for mining large datasets',
 '70','6','Knowledge discovery and mining','5'),

('CS007','Cloud Computing',
 'Cloud fundamentals, IaaS PaaS SaaS, virtualization, containers, Docker, Kubernetes, AWS services (EC2, S3, Lambda), Azure basics, serverless, microservices, deployment pipelines, infrastructure as code, monitoring, autoscaling, distributed storage, cost optimization, cloud security, networking',
 '95','7','Cloud and distributed platforms','5'),

('CS008','Computer Vision',
 'Image processing fundamentals, convolutional neural networks, object detection (YOLO, SSD), image segmentation (U-Net, Mask R-CNN), feature extraction, SIFT SURF, optical flow, face detection, OpenCV pipelines, image augmentation, transfer learning for CV, explainability of vision models, real-time inference',
 '60','8','Image understanding and CV','5'),

('CS009','Information Retrieval',
 'IR systems, inverted index, tokenization, stop words, ranking (tf-idf, BM25), index compression, search architectures, web crawling, query processing, relevance feedback, evaluation metrics (precision, recall, MAP), recommender basics, semantic search, embedding-based retrieval',
 '85','9','Search engines and retrieval','5'),

('CS010','Reinforcement Learning',
 'Markov decision processes, value iteration, policy iteration, Q-learning, SARSA, function approximation, policy gradient methods, actor-critic, deep reinforcement learning, exploration-exploitation trade-off, reward shaping, multi-agent RL, applications in robotics and games, OpenAI Gym practicals',
 '35','10','Learning via interaction','6'),

('CS011','Advanced Databases',
 'Database internals, transactions and concurrency control, isolation levels, recovery, indexing strategies B-tree, bitmap, query optimization, distributed DB, CAP theorem, NewSQL, NoSQL patterns, sharding, replication, columnar stores, OLAP vs OLTP, materialized views, temporal / spatial data handling',
 '120','11','Database internals and scalability','6'),

('CS012','Distributed Systems',
 'Distributed programming models, consensus (Paxos, Raft), leader election, fault tolerance, CAP theorem, distributed transactions, event sourcing, microservices architecture, distributed tracing, consistency models, message queues, replication and partitioning, concurrency and parallelism',
 '75','12','Architecting distributed systems','6'),

('CS013','IoT Systems',
 'Embedded sensors, microcontrollers (ESP32, Arduino), MQTT, CoAP, edge computing, sensor networks, telemetry, data collection pipelines, low-power wireless (BLE, LoRa), security for IoT, device management, cloud integration, prototyping and hardware-software interfacing',
 '50','13','Internet of Things design','6'),

('CS014','Cyber Security',
 'Network security fundamentals, cryptography (symmetric, asymmetric, hashing), TLS/SSL, secure coding, OWASP top10, penetration testing basics, vulnerability scanning, intrusion detection systems, secure architectures, authentication and authorization, malware analysis fundamentals, privacy-preserving tech',
 '140','14','Systems security and hardening','6'),

('CS015','Blockchain Technologies',
 'Blockchain fundamentals, consensus mechanisms (PoW, PoS), smart contract development (Solidity), Ethereum, Hyperledger, decentralized apps, tokenomics, cryptographic primitives, distributed ledgers, gas optimization, decentralized storage, use-cases (supply chain, finance), security pitfalls',
 '28','15','Decentralized systems and smart contracts','6'),

('CS016','Software Architecture',
 'Design patterns (GOF), microservices vs monolith, service decomposition, domain-driven design, UML, architecture trade-offs, scalability and reliability patterns, event-driven architectures, API design, CI/CD pipelines, containerization, testability and monitoring, refactoring large systems',
 '105','16','Architectural design and patterns','6'),

('CS017','Robotics and Control',
 'Robot kinematics and dynamics, control systems PID, sensors and actuators, SLAM, motion planning, ROS, path planning, perception for robotics, simulation (Gazebo), embedded control, hardware interfacing, autonomous navigation',
 '45','17','Robotics foundations','5'),

('CS018','Computer Networks and Wireless',
 'Network layering, TCP/UDP, routing algorithms OSPF BGP basics, wireless protocols (802.11 family), QoS, sockets programming, NAT, VPNs, SDN intro, network security, programmable networks, traffic engineering, performance analysis',
 '130','18','Networking principles and wireless','5');

INSERT INTO Company VALUES
('MI001','Microsoft'),
('AP001','Apple'),
('GO001','Google'),
('AM001','Amazon'),
('NV001','NVIDIA'),
('FB001','Meta');

INSERT INTO Company_Locations VALUES
('MI001','Bengaluru'),
('MI001','Hyderabad'),
('AP001','Cupertino'),
('GO001','Bengaluru'),
('AM001','Seattle'),
('NV001','Santa Clara'),
('FB001','Menlo Park');

INSERT INTO Job VALUES
('MA11MI','Manager','Manager role','MI001'),
('EN11MI','Engineer','Software Engineer','MI001'),
('DS11MI','Data Scientist','Data Science role','MI001'),
('MA11AP','Manager','Manager role','AP001'),
('EN11AP','Engineer','Software Engineer','AP001'),
('EN11GO','Engineer','Software Engineer','GO001'),
('RS11NV','Researcher','Research role','NV001'),
('DS11AM','Data Scientist','Data role','AM001'),
('EN11FB','Engineer','Software Engineer','FB001');


INSERT INTO Projects VALUES
('Smart Traffic Optimizer',2022),
('NLP Chatbot',2021),
('Retail Analytics Dashboard',2023),
('DeepFake Detector',2023),
('Face Recognition System',2022),
('Stock Market Predictor',2023),
('Real-time Object Detection',2023),
('Autonomous Drone Navigation',2023),
('Speech Emotion Recognition',2022),
('Fraud Detection System',2022),
('Crop Disease Classifier',2023),
('Sentiment Analyzer',2021),
('Document Summarizer',2022),
('Movie Recommendation Engine',2021),
('IoT Smart Home Monitor',2023),
('Distributed File Storage',2023),
('Blockchain Voting System',2023),
('Network Intrusion Detector',2022),
('Cloud Resource Scheduler',2023),
('Medical Report Classifier',2023),
('E-commerce Search Engine',2023),
('ChatGPT-like Mini LLM',2024),
('Autonomous Warehouse Robot',2023),
('Satellite Image Analysis',2024);

INSERT INTO Student VALUES
('S001','Aisha Sharma',9.12,'2000-03-12',2022),
('S002','Ravi Kumar',8.25,'1999-07-30',2021),
('S003','Neha Singh',8.90,'2000-11-05',2022),
('S004','Tarun Mehta',9.00,'2000-01-01',2021),
('S005','Anjali V',8.50,'2000-02-02',2022),
('S006','Karan Patel',8.80,'1998-05-05',2020),
('S007','Priya Desai',8.20,'1999-08-08',2021),
('S008','Manish Rao',7.95,'1998-12-12',2020),
('S009','Sonal Gupta',9.05,'2001-06-06',2023),
('S010','Vikram Singh',8.10,'2000-09-09',2022),
('S011','Divya Nair',8.75,'1999-04-04',2021),
('S012','Rohit Sharma',7.80,'1997-11-11',2019);

INSERT INTO Belongs_To VALUES
('S001','CS001','Loved advanced algos',88),
('S002','CS002','Very practical',78),
('S003','CS003','Challenging but useful',60),
('S004','CS004','Great NLP topics',92),
('S005','CS005','DL projects fun',70),
('S006','CS006','Mining was practical',85),
('S007','CS007','Cloud labs were great',90),
('S008','CS008','CV assignments hard',75),
('S009','CS009','IR was eye-opening',80),
('S010','CS017','Robotics intro',82),
('S011','CS018','Networking strong',79),
('S012','CS011','Advanced DBs deep',74),

('S001','CS006','mining extra projects',86),
('S002','CS007','cloud exposure',88),
('S003','CS008','cv mini-project',70),
('S004','CS009','search index project',78),
('S005','CS010','rl simple agent',55),
('S006','CS011','db internals',91),
('S007','CS012','distributed labs',83),
('S008','CS013','iot prototypes',65),
('S009','CS014','security baseline',92),
('S010','CS015','blockchain hack',60),
('S011','CS016','architecture case studies',87),
('S012','CS004','nlp basics',69),

('S001','CS002','eda and viz',90),
('S002','CS003','spark pipelines',77),
('S003','CS005','dl special topics',66),
('S004','CS001','graphs project',84),
('S005','CS009','search relevance',72);


INSERT INTO Project_Guide VALUES
('S001','Smart Traffic Optimizer','TE000'),
('S002','NLP Chatbot','TE003'),
('S003','DeepFake Detector','TE008'),
('S004','Distributed File Storage','TE007'),
('S005','Blockchain Voting System','TE011'),
('S006','Speech Emotion Recognition','TE002'),
('S007','Stock Market Predictor','TE009'),
('S008','Network Intrusion Detector','TE010'),
('S009','Crop Disease Classifier','TE004'),
('S010','Autonomous Drone Navigation','TE006'),
('S011','ChatGPT-like Mini LLM','TE001'),
('S012','Autonomous Warehouse Robot','TE006');


INSERT INTO Works_On VALUES
('S001','MI001','EN11MI'),
('S002','AP001','MA11AP'),
('S003','GO001','EN11GO'),
('S004','NV001','RS11NV'),
('S005','AM001','DS11AM'),
('S006','MI001','DS11MI'),
('S007','AP001','EN11AP'),
('S008','GO001','EN11GO'),
('S009','AM001','DS11AM'),
('S010','NV001','RS11NV'),
('S011','FB001','EN11FB'),
('S012','MI001','EN11MI');

INSERT INTO Taught_By VALUES
('S001','CS001','TE000'),
('S001','CS002','TE000'),
('S002','CS007','TE001'),
('S003','CS003','TE002'),
('S004','CS004','TE003'),
('S005','CS005','TE004'),
('S006','CS006','TE005'),
('S007','CS007','TE006'),
('S008','CS008','TE007'),
('S009','CS009','TE004'),
('S010','CS017','TE009'),
('S011','CS018','TE010'),
('S012','CS011','TE011');