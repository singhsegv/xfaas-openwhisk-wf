const composer = require("openwhisk-composer");

module.exports = composer.sequence("/guest/graphs/graph_gen", composer.parallel("/guest/graphs/graph_bft", "/guest/graphs/pagerank", "/guest/graphs/graph_mst"), "/guest/graphs/aggregate");
// module.exports = composer.sequence("/guest/graphs/graph_gen", "/guest/graphs/graph_bft", "/guest/graphs/aggregate");
