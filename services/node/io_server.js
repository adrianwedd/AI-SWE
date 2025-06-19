const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const packageDef = protoLoader.loadSync(path.join(__dirname, '../../proto/io_service.proto'));
const proto = grpc.loadPackageDefinition(packageDef).aiswa;

function ping(call, callback) {
  callback(null, { message: 'pong:' + call.request.message });
}

function main() {
  const server = new grpc.Server();
  server.addService(proto.IOService.service, { Ping: ping });
  const port = process.env.PORT || '50051';
  server.bindAsync('0.0.0.0:' + port, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log(`IOService running on ${port}`);
  });
}

if (require.main === module) {
  main();
}

module.exports = { ping };
