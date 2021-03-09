# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

FROM ndourbae/ultroid:beta1.0

WORKDIR /root/TeamUltroid/
RUN git clone -b beta https://github.com/xscrprog/Ultroid.git
RUN pip install -r requirements.txt
CMD ["bash", "resources/startup/startup.sh"]