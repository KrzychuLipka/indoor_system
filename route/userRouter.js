const express = require('express');
const router = express.Router();
const userService = require('../service/userService');

router.get('/', async function(req, res, next) {
  try {
    res.json(await userService.getAll());
  } catch (error) {
    console.error(`Error while fetching users.`, error.message);
    next(error);
  }
});

router.post('/', async function(req, res, next) {
  try {
    res.json(await userService.save(req.body));
  } catch (err) {
    console.error(`User saving error.`, err.message);
    next(err);
  }
});

router.put('/:id', async function(req, res, next) {
  try {
    res.json(await userService.update(req.params.id, req.body));
  } catch (err) {
    console.error(`Error while updating user.`, err.message);
    next(err);
  }
});

router.delete('/:id', async function(req, res, next) {
  try {
    res.json(await userService.remove(req.params.id));
  } catch (err) {
    console.error(`Error while deleting user.`, err.message);
    next(err);
  }
});

module.exports = router;