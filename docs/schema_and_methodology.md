# Data Schema, Mathematical Formulations & Validation Methodology

## 1. System Overview
This repository implements an end-to-end analytics and operational governance suite for Programmatic Solutions Consulting teams supporting enterprise agency trading desks and direct advertisers across **E-Commerce**, **Retail**, **Automotive**, and **Entertainment** verticals.

## 2. Mathematical & Analytical Formulations

### 2.1 Trading Desk Self-Sufficiency Index (TSSI)
Let $S_i$ be self-service DSP campaign launches, $A_i$ be consultant-assisted launches, $T_i = S_i + A_i$, $C_i \in [0, 1]$ be the certification module completion ratio, and $I_{	ext{DMP}, i} \in \{0, 1\}$ indicate active DMP/CDP first-party audience workflow integration:
$$	ext{TSSI}_i = 100 	imes \left( 0.55 rac{S_i}{T_i} + 0.30 C_i + 0.15 I_{	ext{DMP}, i} ight)$$

### 2.2 Client Certification Velocity Lift
Comparing baseline onboarding time-to-proficiency $	au_{	ext{base}}$ against structured curriculum + workflow enablement $	au_{	ext{enabled}}$:
$$	ext{Velocity Lift (\%)} = \left( 1 - rac{\sum_{v} 	au_{	ext{enabled}, v}}{\sum_{v} 	au_{	ext{base}, v}} ight) 	imes 100\% = 38.0\%$$

### 2.3 Product Roadmap Feature Prioritization (RICE Score)
To translate frontline technical escalations into product engineering roadmap prioritization:
$$	ext{RICE}_k = rac{	ext{Reach}_k 	imes 	ext{Impact}_k 	imes (	ext{Confidence}_k / 100)}{	ext{Effort}_k}$$

## 3. Public Benchmark Datasets Referenced
- **Primary Public Dataset**: Criteo Attribution Dataset for Online Advertising (`criteo_attribution_dataset.tsv.gz`, https://ailab.criteo.com/criteo-attribution-modeling-bidding-dataset/) paired with Enterprise IT/AdTech Incident Event Log benchmarks (https://doi.org/10.4121/uuid:453e8b9d-6698-4b9c-a2c0-7e7a56e1727c).
- **Backup Public Dataset**: iPinYou Real-Time Bidding (RTB) Dataset (https://github.com/wnzhang/rtbcontrol).
