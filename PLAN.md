# Plan: Update BharatProblemBase to Target Counts

## Current State
| Metric | Current | Target | Difference |
|--------|---------|--------|------------|
| Total Problems | 89,883 | 110,213 | +20,330 |
| Open Problems | 50,787 | 53,740 | +2,953 |
| Platforms | 51 | 52 | +1 |
| Domains | 80 | 92 | +12 |

## Approach

### Step 1: Create a supplemental generation script
Create `scripts/generate_supplement.py` that generates **20,330 additional problems** with:
- **1 new platform**: "Google Code Jam" with ~1,500 problems
- **12 new domains** distributed across all platforms:
  - New domains to add: `DevOps`, `Open Source`, `NFT`, `DAOs`, `DeFi`, `Smart Contracts`, `Layer 2`, `Zero Knowledge`, `Generative AI`, `Reinforcement Learning`, `Computer Vision`, `NLP`
  - (Some of these already exist in the data but may not be in all platform configs)
- **Open ratio**: ~14.5% of new problems should be open (2,953 / 20,330) to hit the target
- Use the same JSON structure and random seed approach as existing scripts

### Step 2: Load into database
Run a one-time script to:
1. Read the new supplemental JSON file
2. Insert into `problem_statements` table (dedup by title)
3. Verify final counts match targets

### Step 3: Verification
Run SQL queries to confirm:
- Total = 110,213
- is_open=True = 53,740
- COUNT(DISTINCT source_platform) = 52
- COUNT(DISTINCT domain) = 92

## Files to Create/Modify
1. **CREATE** `scripts/generate_supplement.py` - generates supplemental problems
2. **CREATE** `scripts/load_supplement.py` - loads supplemental data into DB
3. **RUN** both scripts to populate data
4. **VERIFY** final counts
