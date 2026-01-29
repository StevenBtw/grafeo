//! # grafeo-adapters
//!
//! Adapters layer for Grafeo: storage backends, query language parsers,
//! and plugin interfaces.
//!
//! ## Modules
//!
//! - [`storage`] - Storage backends (memory, mmap, WAL)
//! - [`query`] - Query language parsers (GQL, Cypher)
//! - [`plugins`] - Plugin system and bridges

pub mod plugins;
pub mod query;
pub mod storage;
