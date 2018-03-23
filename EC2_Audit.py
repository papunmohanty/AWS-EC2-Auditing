#!/usr/bin/python3

import boto3
import pandas as pd


class AmazonEC2Audit():
    '''
    Class to generate Excel Report for the required EC2 environment details.
    '''
    def instance_name_filter(self, instance):
        # Trying to get the Instance Name in below try block
        try:
            for i in instance['Tags']:
                if i["Key"] == "Name":
                    self.instance_name.append(i["Value"])
        except:
            pass

    def instance_id_filter(self, instance):
        self.instance_id.append(instance["InstanceId"])

    def instance_type_filter(self, instance):
        self.instance_type.append(instance["InstanceType"])

    def instance_platform_filter(self, instance):
        # for getting Platform (Linux/Windows) detail
        try:
            self.instance_platform.append(instance["Platform"])
        except KeyError:
            self.instance_platform.append("Linux")

    def instance_state_filter(self, instance):
        self.instance_state.append(instance["State"]["Name"])

    def instance_availability_zone_filter(self, instance):
        self.instance_availability_zone.append(instance["Placement"]["AvailabilityZone"])

    def instance_vpc_id_filter(self, instance):
        self.instance_vpc_id.append(instance["VpcId"])

    def instance_launch_time_filter(self, instance):
        self.instance_instance_launch_time.append(instance["LaunchTime"])

    def instance_security_group_filter(self, instance):
        '''
        SG appending process
        '''
        sg = []
        for item in instance["NetworkInterfaces"][0]["Groups"]:
            sg.append(item["GroupId"])

        self.instance_security_group.append(', '.join(sg))
        sg = []


    def testing_instance_details(self):
        '''
        Testing for Instance detail status prior to pushing data to an Excel Sheet
        '''
        print("==============={} Account, {} Region=====================".format(self.environment.capitalize(), self.region))
        print("Total Instance Names is ", len(self.instance_name))
        print("Total Instances are ", len(self.instance_id))
        print("Total Instance Types are ", len(self.instance_type))
        print("Total Instance Platform is ", len(self.instance_platform))
        print("Total Instance States are ", len(self.instance_state))
        print("Total Instance Availability zones are ", len(self.instance_availability_zone))
        print("Total Instance VPC ID is ", len(self.instance_vpc_id))
        print("Total Instance Launch Time is ", len(self.instance_instance_launch_time))
        print("Total SG length is ", len(self.instance_security_group))


    def data_frame_generation(self):
        '''
        Data Frame generation
        '''
        self.df_ec2 = pd.DataFrame({
            'Instance_Name': self.instance_name,
            'Instance_ID': self.instance_id,
            'Instance_Type': self.instance_type,
            'Instance_Platform': self.instance_platform,
            'Instance_State': self.instance_state,
            'Availability_Zone': self.instance_availability_zone,
            'VPC_Id': self.instance_vpc_id,
            'Instance_Launch_Time': self.instance_instance_launch_time,
            'Security_Groups': self.instance_security_group,
        })
        print("Data frame generated successfully for {} Environment".format(self.environment.capitalize()))


    def generate_excel_report(self):
        '''
        Pushing All data frame to an excel sheet
        '''
        with pd.ExcelWriter('ec2Audit_{}_{}.xlsx'.format(self.environment.capitalize(), self.region)) as writer:
            self.df_ec2.to_excel(writer, sheet_name='{}_aws_{}'.format(self.environment, self.region))


    def __init__(self, env, region):
        self.environment = env
        self.region = region

        # Variable initializations for required instance attributes
        self.instance_name = []
        self.instance_id = []
        self.instance_type = []
        self.instance_platform = []
        self.instance_state = []
        self.instance_availability_zone = []
        self.instance_vpc_id = []
        self.instance_instance_launch_time = []
        self.instance_security_group = []

        # Creating a session to the given environment with corresponding region
        self.ec2client = boto3.Session(profile_name=self.environment).client('ec2', region_name=self.region)

        # Creating a response object that saves the environment data to this object
        self.response = self.ec2client.describe_instances()

    def ec2_resource_iteration(self):
        for reservation in self.response["Reservations"]:
            for instance in reservation["Instances"]:
                # method call to filter instance Names
                self.instance_name_filter(instance)

                # method call to filter instance id
                self.instance_id_filter(instance)

                # method call to filter instance type
                self.instance_type_filter(instance)

                # method call to filter instance platform
                self.instance_platform_filter(instance)

                # method call to filter instance state
                self.instance_state_filter(instance)

                # method call to filter instance availability zone
                self.instance_availability_zone_filter(instance)

                # method call to filter vpc id
                self.instance_vpc_id_filter(instance)

                # method call to filter instance launch time
                self.instance_launch_time_filter(instance)

                # method call to filter instance security group
                self.instance_security_group_filter(instance)

        self.testing_instance_details()

        self.data_frame_generation()

        self.generate_excel_report()


if __name__ == "__main__":

    environment_input = input("Enter the Environment Name: ")
    region_input = input("Enter the Region Name: ")
    prod_audit = AmazonEC2Audit(environment_input, region_input)
    prod_audit.ec2_resource_iteration()
