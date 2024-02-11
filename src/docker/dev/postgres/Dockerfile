
FROM postgres:15-bullseye

# this is done for self-hosting database and backups
# copy host maintenance dir to the container
COPY ./docker/dev/postgres/maintenance /usr/local/bin/maintenance

# give executable permission 
RUN chmod +x /usr/local/bin/maintenance/* 

# move the all files in the container's maintenance dir into the bin dir and delete the maintenance dir 
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance


