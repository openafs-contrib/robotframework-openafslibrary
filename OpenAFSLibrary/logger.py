# Copyright (c) 2014-2025 Sine Nomine Associates
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import os
import datetime
import robot.api.logger


def _is_robot_api_logger_enabled():
    logging = os.getenv("ROBOT_API_LOGGER", "no").lower()
    return logging in ["true", "yes", "1", "enable", "enabled"]


def _write(msg, **kargs):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{now} {msg}")


if _is_robot_api_logger_enabled():
    trace = robot.api.logger.trace
    debug = robot.api.logger.debug
    info = robot.api.logger.info
    warn = robot.api.logger.warn
    error = robot.api.logger.error
else:
    trace = _write
    debug = _write
    info = _write
    warn = _write
    error = _write
