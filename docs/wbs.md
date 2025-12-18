 # Work Breakdown Structure (WBS) – Race Performance Intelligence System (RPIS)

## 1.0 Project management
- 1.1 Define project charter and scope
- 1.2 Create WBS and Gantt chart
- 1.3 Weekly progress review and adjustments
- 1.4 Final report and presentation

## 2.0 Data infrastructure
- 2.1 Set up development environment (Python, virtual environment, Git)
- 2.2 Integrate FastF1 and configure data caching
- 2.3 Define data schema for laps, stints, and tyres
- 2.4 Implement data validation and basic sanity checks

## 3.0 Analysis and modelling
- 3.1 Implement lap time and sector analysis
- 3.2 Implement stint segmentation (based on pit stops and tyre compounds)
- 3.3 Develop initial tyre degradation model (simple regression-based)
- 3.4 Implement simple strategy scenario comparison (e.g., 1-stop vs 2-stop)

## 4.0 Dashboard and user interface
- 4.1 Design dashboard layout and user flows (wireframe)
- 4.2 Implement basic Streamlit app structure
- 4.3 Add lap and stint visualization components
- 4.4 Add strategy comparison interface and results view

## 5.0 Testing and validation
- 5.1 Write unit tests for core data processing functions
- 5.2 Conduct integration tests for end-to-end race analysis
- 5.3 Validate model outputs against known race results (qualitative)

## 6.0 Deployment and documentation
- 6.1 Prepare requirements.txt and configuration files
- 6.2 Deploy dashboard to a cloud platform (e.g., Streamlit Cloud/Render)
- 6.3 Create deployment guide and usage instructions
- 6.4 Compile final documentation and project summary