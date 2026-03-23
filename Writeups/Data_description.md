## **About the online_shoppers_intention.csv dataset**

The online_shoppers_intention.csv dataset contains 12,330 sessions and 18 features describing user behavior in an online retail store. It captures both behavioral metrics and contextual attributes for each session:


<span style="font-size:115%"><b>Session Activity:</b></span>

> **`Administrative`** & **`Administrative_Duration`**
- **`Administrative`**, **`Administrative_Duration`**
    - Counts and total time spent on administrative pages (e.g., account info).
- **`Informational`**, **`Informational_Duration`**
    - Counts and time spent on informational pages (e.g., FAQs).
- **`ProductRelated`**, **`ProductRelated_Duration`**
    - Counts and time spent on product pages.

<span style="font-size:115%"><b>Engagement & Value Metrics:</b></span>

- **`BounceRates`**
    - Percentage of visitors leaving after one page.
- **`ExitRates`**
    - \[
\text{Session ExitRate} = \frac{\text{Total exits in session}}{\text{Total pageviews in session}}
\]

- **`PageValues`**
    - Estimated monetary value of the page based on e-commerce analytics.

<span style="font-size:115%"><b>Contextual & Temporal Factors:</b></span>

- **`SpecialDay`**
    - Proximity of the visit to a special day (e.g., Valentine’s).
- **`Month`**
    - Month of visit.
- **`Weekend`**
    - Whether the session occurred on a weekend.

<span style="font-size:115%"><b>Technical & Demographic Proxies:</b></span>

- **`OperatingSystems`**
    - Encoded categorical variable describing the user's operating system.
- **`Browser`**
    - Encoded categorical variable describing the user's browser.
- **`Region`**
    - Encoded categorical variable describing the user's region.
- **`TrafficType`**
    - Encoded categorical variable describing the user's traffic source.
- **`VisitorType`**
    - Indicates whether the user is a new or returning visitor.

**Outcome variable:**

- **`Revenue`**
    - Boolean flag indicating whether the session resulted in a purchase.

This dataset is well-suited to value alignment analysis because it contains observable actions (page visits, time spent, exit behavior) alongside context variables (special day, weekend) that can be used to infer preferences and test alignment under different conditions. Considering the healthy number of datapoints, and the appropriate features available I chose the question: 

# **Can we infer shopper preferences probabilistically from behavioral data, and evaluate how consistently their actions align with these preferences under contextual shifts such as holidays, weekends, or peak shopping periods? Further, can we define a rationality score to quantify the degree of alignment between inferred goals and observed decisions?**