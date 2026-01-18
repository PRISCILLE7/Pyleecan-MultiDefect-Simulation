# Generation and Simulation of Multi-Defect Electric Machines for the Construction of a Dataset Dedicated to AI-Assisted Fault Diagnosis

##  Project Overview

This internship / master’s thesis project focuses on the **generation and simulation of electric machines with multiple defects** using the open-source framework **Pyleecan**.  
The main objective is to build a **structured and labeled dataset of physical signals** (electromagnetic torque, magnetic flux density, currents, etc.) under various faulty operating conditions, dedicated to **AI-assisted fault diagnosis**.

The project combines **electromagnetic simulation**, **fault modeling**, and **data generation** for **predictive maintenance and machine learning applications**.

---

##  Objectives

- Automatically generate electric machines with customized parameters  
- Simulate **multiple defect types** (geometrical, magnetic, electrical)  
- Analyze the impact of defects on machine behavior  
- Build datasets for **machine learning and fault diagnosis**  
- Compare healthy vs faulty machine performances  

---

##  Project Structure

    ```text
    Tutorials/
    ├── 01_tuto_Machine.ipynb                 # Main tutorial notebook
    │
    ├── MACHINE_TESLA_MODEL_3/                # Tesla Model 3 analysis & generation
    │   ├── Analyse_de_la_machine.ipynb
    │   ├── machine_generator_tesla.ipynb
    │   ├── Machines_defaut_usinages.ipynb
    │   └── (large datasets excluded from GitHub)
    │
    ├── MACHINE_TOYOTA_PRUIS/                 # Toyota Prius machine studies
    │   ├── 01_tuto_Machine.ipynb
    │   ├── 02_tuto_Simulation_FEMM.ipynb
    │   ├── machine_generator_toyota_pruis.ipynb
    │   └── Winding_Failure_Simulation.ipynb
    │
    ├── machines_custom_batch_ntcoil/         # Batch simulations
    │   └── code/                             # Source code only
    │
    ├── article-slf/                          # Publication-related notebooks
    │
    ├── serie/                                # CSV exports (excluded from GitHub)
    │
    ├── thesis/                               # Master’s thesis (PDF)
    │
    └── README.md


##  Important Note

Large datasets, simulation outputs, and generated results are **not tracked on GitHub** due to their size.  
They must be generated **locally** using the provided scripts and notebooks.

---

##  Technologies Used

- **Pyleecan (v1.5.2)** – Electric machine simulation framework  
- **SciDataTool (v2.5.0)** – Scientific data processing  
- **FEMM** – Finite Element Method Magnetics  
- **Python** – Main programming language  
- **Jupyter Notebook** – Analysis and prototyping  
- **NumPy, Pandas, Matplotlib, SciPy** – Scientific computing  
- **PyTorch** – Deep learning framework (fault diagnosis experiments)

---

##  Studied Electric Machines

### Tesla Model 3 – IPMSM
- Interior Permanent Magnet Synchronous Machine  
- Machining tolerances and geometrical defects  
- Air-gap variations (±5%, ±10%)  
- Magnet demagnetization scenarios  

### Toyota Prius 2004 – IPMSM
- Reference traction machine  
- Winding and inter-turn short-circuit faults  
- Coil number (Ntcoil) variations  
- Magnetic and geometrical sensitivity analyses  

---

##  Types of Defects Analyzed

### Geometrical Defects
- Rotor–stator eccentricity  
- Machining tolerances (±0.5% to ±10%)  
- Air-gap variations  

### Magnetic Defects
- Partial and severe demagnetization  
- Magnet property degradation  

### Electrical Defects
- Inter-turn short circuits  
- Winding failures  
- Coil number variations (Ntcoil)  

### Material Defects
- Magnetic material property variations  

---

##  Main Features

### Machine Generation
- Automatic machine generation from parametric definitions  
- **Boldea-based analytical sizing approach**  
- Physical constraint validation  

### Simulation
- Finite Element electromagnetic simulations (FEMM)  
- Computation of torque, flux density, and currents  
- FFT and spectral analysis  
- 2D/3D visualization of machines  

### Batch Processing
- Large-scale batch simulation of electric machines  
- Automated classification of simulated / non-simulated cases  
- Structured organization of simulation results  

### Data Generation for AI
- Dataset construction for machine learning  
- Feature extraction in time and frequency domains  

---

##  Datasets & Results

 **Datasets and simulation results are not included in this repository.**

They consist of:
- JSON machine configurations  
- Simulation outputs  
- CSV exports  
- Flux maps and FFT visualizations  

All datasets can be **reproduced locally** using the provided notebooks.

---

##  Getting Started

### Prerequisites
- Python **3.10+**  
- FEMM installed locally  
- Dependencies listed in:
    MACHINE_TOYOTA_PRUIS/requirements.txt
  
## Installation
`
pip install -r MACHINE_TOYOTA_PRUIS/requirements.txt
`
##  Example Notebooks

- `01_tuto_Machine.ipynb`  
- `machine_generator_tesla.ipynb`  
- `machine_generator_toyota_pruis.ipynb`  

---

##  Academic & Industrial Context

This project was carried out in the framework of a **Master’s thesis and research internship**, in collaboration with academic and industrial partners:

- **Institut Francophone International (IFI)** – Vietnam National University (VNU), Hanoi  
- **University of La Rochelle**, France  
- **LGI2A Laboratory** – Université d’Artois, France  
- **EDF (Électricité de France)** – Industrial partner  

### Master’s Thesis

- **Title**:  
  *Generation and Simulation of Multi-Defect Electric Machines for the Construction of a Dataset Dedicated to AI-Assisted Fault Diagnosis*  
- **Author**: Priscille E. Ebwala  
- **Year**: 2025  

---

##  Contributions

This project was developed in an academic research context.  
For any questions or collaboration inquiries, please contact the author.

---

##  Notes

- FEM simulations can be computationally expensive  
- Some machine configurations may fail to converge  
- Large datasets must be stored locally or on dedicated storage platforms  

---

##  References

- Pyleecan GitHub: https://github.com/Eomys/pyleecan  
- Pyleecan Documentation: https://www.pyleecan.org/  
- Boldea, I., & Nasar, S. A., *Electric Drives*  

---

**Author**: Priscille E. Ebwala  
**Year**: 2025  
**Version**: 1.0


