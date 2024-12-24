/*
 * This script patches and introduces the `haunt` functions
 * into the global context.
 *
 * TODO: Implement a minified version
 */

function defineHaunt(global) {
  global.haunt = new Proxy(
    {
      /**
       * @typedef {Object} BindEntry
       * @property {Function} func - The callback of the function.
       * @property {boolean} isAsync - Indicates if the function is asynchronous.
       */

      /**
       * An object that stores bindings.
       * The keys are strings, and the values are objects of type BindEntry.
       * @type {Object<string, BindEntry>}
       */
      _binds: {},

      _exec_bind: function (packedData) {
        let unpackedData = JSON.parse(packedData);
        let funcName = unpackedData.funcName;
        let args = unpackedData.args;

        if (!(funcName in this._binds)) {
          throw Error(
            "Attempted to call a non-existent function within inner JS bind map.",
          );
        }

        let func = this._binds[funcName];
        return func.func(...args);
      },

      bind: function (callback, funcName, isAsync = false) {
        window.pywebview.api.bind_function(funcName, isAsync);
        this._binds[funcName] = {
          func: callback,
          isAsync: isAsync,
        };
      },
    },
    {
      get(target, prop, receiver) {
        if (prop in target) {
          return Reflect.get(target, prop, receiver);
        }

        return async function (...args) {
          return await window.pywebview.api.call_function(prop, args);
        };
      },
    },
  );
}

defineHaunt(window);
