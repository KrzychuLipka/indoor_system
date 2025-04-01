const db = require('../db');
const utils = require('../utils');
const config = require('../config');

async function getAll() {
  const result = await db.query(`SELECT id, name, latitude, longitude FROM user`)
  return utils.getData(result);
}

async function save(user) {
  const result = await db.query(
    `INSERT INTO user (name, latitude, longitude) VALUES ('${user.name}', '${user.latitude}', '${user.longitude}')`);
  let message = 'Error during saving user.';
  if (result.affectedRows) {
    message = 'User saved successfully.';
  }
  return {message};
}

async function update(id, user){
  const result = await db.query(
    `UPDATE user SET name="${user.name}", latitude="${user.latitude}", longitude="${user.longitude}" WHERE id=${id}` 
  );
  let message = 'Error during updating user.';
  if (result.affectedRows) {
    message = 'User updated successfully';
  }
  return {message};
}

async function remove(id){
  const result = await db.query(
    `DELETE FROM user WHERE id=${id}`
  );
  let message = 'Error during deleting user.';
  if (result.affectedRows) {
    message = 'User deleted successfully.';
  }
  return {message};
}

module.exports = {
  getAll,
  save,
  update,
  remove
}