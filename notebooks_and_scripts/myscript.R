# Load core library
library(tidyverse)

# 1. Load data and clean column names/whitespaces
df <- read_csv("customer_raw.csv") %>% 
  distinct() %>% 
  mutate(across(where(is.character), str_trim))

# 2. Fix the CamelCase bug using a Regex lookahead/lookbehind equivalent in R
df <- df %>% 
  mutate(escalation_reason = str_replace_all(escalation_reason, "(?<=[a-z])(?=[A-Z])", " ")) %>% 
  mutate(across(c(region, escalation_reason), str_to_title)) %>% 
  mutate(home_store = str_to_upper(str_replace_all(home_store, " ", "-")))

# 3. Standardize dates and handle future placeholders safely
df <- df %>% 
  mutate(
    signup_date = parse_date_time(signup_date, orders = c("ymd", "ydm"), quiet = TRUE),
    signup_date = if_else(is.na(signup_date), as.POSIXct("2026-01-01"), signup_date)
  )

# 4. Filter down and aggregate data for visual validation
escalation_summary <- df %>% 
  filter(has_escalation %in% c("True", "TRUE", "Y", "Yes", "1")) %>% 
  filter(!is.na(escalation_reason) & escalation_reason != "None" & escalation_reason != "Unknown") %>% 
  group_by(escalation_reason) %>% 
  summarise(
    total_complaints = n(),
    revenue_at_risk = sum(total_spent, na.rm = TRUE)
  ) %>% 
  arrange(desc(revenue_at_risk))

# 5. Create a high-quality portfolio visualization using ggplot2
ggplot(escalation_summary, aes(x = reorder(escalation_reason, revenue_at_risk), y = revenue_at_risk)) +
  geom_col(fill = "#1170E2", width = 0.7) +
  coord_flip() +
  scale_y_continuous(labels = scales::dollar_format()) +
  theme_minimal(base_size = 13) +
  labs(
    title = "Revenue at Risk by Operational Escalation",
    subtitle = "Analysis handled via tidyverse pipeline execution",
    x = "Escalation Reason",
    y = "Total Revenue Impact"
  ) +
  theme(
    plot.title = element_text(face = "bold", size = 16),
    panel.grid.minor = element_blank()
  )
