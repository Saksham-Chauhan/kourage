def create_sqlite_cmd(cursor_name, table_name, _dict):
    cmd = cursor_name + ".execute('''INSERT INTO " + table_name + '('
    for i in _dict:
        cmd += i + ','
    cmd = cmd[:-1] + ') VALUES ('
    for i in _dict:
        cmd += '?,'
    cmd = cmd[:-1] + ")''', ("
    for i in _dict:
        cmd += _dict[i] + ','
    cmd = cmd[:-1] + '))'
    return cmd

def sqlite_fetch_cmd(cursor_name, _dict, primary_key, primary_key_val):
    table_name = None
    for i in _dict:
        table_name = i
    cmd = cursor_name + ".execute('''SELECT "
    for data in _dict[table_name]:
        cmd += data + ","
    cmd = cmd[:-1] + " FROM " + table_name + " WHERE " + primary_key
    cmd += " = ?''', (" + primary_key_val + ",))"

    return table_name, cmd

def sqlite_exist_in_table(cursor_name, table_name, primary_key, primary_key_val):
    cmd = cursor_name + ".execute('''SELECT EXISTS(SELECT 1 FROM "
    cmd += table_name + " WHERE " + primary_key + "=?)''', (" + primary_key_val + ",))"
    return cmd

def sqlite_delete_row(cursor_name, table_name, primary_key, primary_key_val):
    cmd = cursor_name + ".execute('''DELETE FROM "
    cmd += table_name + " WHERE " + primary_key + "=?''', (" + primary_key_val + ",))"
    return cmd
