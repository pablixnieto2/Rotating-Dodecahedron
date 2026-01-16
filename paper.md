---
title: 'Cosmic-Scanner: Autonomous Topological Defect Detection in CMB Data'
tags:
  - python
  - cosmology
  - astrophysics
  - topology
  - big data
  - computer vision
  - cmb
authors:
  - name: Pablo Miguel Nieto Muñoz
    orcid: 0009-0006-2884-9366
    affiliation: 1
affiliations:
 - name: Independent Researcher, Spain
   index: 1
date: 16 January 2026
bibliography: paper.bib
---

# Summary

Modern cosmology relies heavily on statistical analysis of the Cosmic Microwave Background (CMB). However, traditional methods often overlook non-Gaussian geometric anomalies. `Cosmic-Scanner` is a Python library designed to bridge the gap between Big Data analytics and theoretical topology. It implements autonomous agents ("Spider" algorithms) that perform ridge-tracking on spherical data maps to identify coherent structures amidst high-noise environments.

The software includes a suite of tools for:

1. **Autonomous Tracing:** A recursive `bloodhound_tracer` that follows correlation gradients.
2. **Topological Microscopy:** Tools like `viz_vertex_microscope` to analyze vector convergence at vertices.
3. **Global Mapping:** The `full_dodecahedron_map` script capable of projecting Platonic solid geometries onto celestial coordinates.

# Statement of need

Researchers analyzing Planck PR4 data [@Planck:2020] often lack tools to detect linear topological defects ("scars"). Standard Gaussian analysis effectively filters out these linear discontinuities, treating them as noise. `Cosmic-Scanner` solves this by treating the CMB analysis as a computer vision and graph theory problem, rather than a purely statistical one.

This software was instrumental in the research paper "Computational Fractal Cosmology" [@Nieto:2025], identifying potential evidence of a dodecahedral topology with high statistical significance ($82.98\sigma$). While developed for the search of cosmic topology, specifically the Poincaré Dodecahedral Space [@Luminet:2003], the algorithms are agnostic and can be applied to any spherical dataset requiring ridge detection or geometric pattern matching.

# Key Features

* **Ridge Tracking**: Implementation of autonomous agents that traverse the spherical surface seeking maximum Temperature-Polarization (T-P) correlations.
* **Kaiser-Stebbins Detection**: Automated profiling of temperature steps orthogonal to detected ridges.
* **Geometric Validation**: Scripts to verify the chirality and Eulerian characteristics of the detected meshes.

# References
