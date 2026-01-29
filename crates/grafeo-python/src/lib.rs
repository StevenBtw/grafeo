//! Python bindings for Grafeo graph database.
//!
//! This crate provides Python bindings via PyO3, exposing the core
//! graph database functionality to Python users.

#![warn(missing_docs)]

use pyo3::prelude::*;

mod bridges;
mod database;
mod error;
mod graph;
mod query;
mod types;

use bridges::{PyAlgorithms, PyNetworkXAdapter, PySolvORAdapter};
use database::{AsyncQueryResult, AsyncQueryResultIter, PyGrafeoDB};
use graph::{PyEdge, PyNode};
use query::PyQueryResult;
use types::PyValue;

/// Grafeo Python module.
#[pymodule]
fn grafeo(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyGrafeoDB>()?;
    m.add_class::<PyNode>()?;
    m.add_class::<PyEdge>()?;
    m.add_class::<PyQueryResult>()?;
    m.add_class::<AsyncQueryResult>()?;
    m.add_class::<AsyncQueryResultIter>()?;
    m.add_class::<PyValue>()?;
    m.add_class::<PyAlgorithms>()?;
    m.add_class::<PyNetworkXAdapter>()?;
    m.add_class::<PySolvORAdapter>()?;

    // Add version info
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    Ok(())
}
