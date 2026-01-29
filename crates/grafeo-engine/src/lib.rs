//! # grafeo-engine
//!
//! The main entry point for Grafeo: database management, transactions,
//! query processing, and optimization.
//!
//! ## Modules
//!
//! - [`database`] - GrafeoDB struct and lifecycle management
//! - [`session`] - Session/Connection management
//! - [`config`] - Configuration options
//! - [`transaction`] - Transaction management and MVCC
//! - [`query`] - Query processing, binding, planning, optimization, execution
//! - [`catalog`] - Schema and index catalog

pub mod catalog;
pub mod config;
pub mod database;
pub mod query;
pub mod session;
pub mod transaction;

pub use catalog::{Catalog, CatalogError, IndexDefinition, IndexType};
pub use config::Config;
pub use database::GrafeoDB;
pub use session::Session;
