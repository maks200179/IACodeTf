variable "region" {
  default = "us-east-2"
}

variable "map_accounts" {
  description = "Additional AWS account numbers to add to the aws-auth configmap."
  type        = list(string)

  default = [
    "411543714039",
  ]
}

variable "map_roles" {
  description = "Additional IAM roles to add to the aws-auth configmap."
  type = list(object({
    rolearn  = string
    username = string
    groups   = list(string)
  }))

  default = [
    {
      rolearn  = "arn:aws:iam::411543714039:role/eks-managed-group-node-role"
      username = "terra"
      groups   = ["system:masters"]
    },
    {
      rolearn  = "arn:aws:iam::411543714039:role/eks-managed-group-node-role"
      username = "system:node:{{EC2PrivateDNSName}}"
      groups   = ["system:bootstrappers","system:nodes"]
    },
  ]
}

variable "map_users" {
  description = "Additional IAM users to add to the aws-auth configmap."
  type = list(object({
    userarn  = string
    username = string
    groups   = list(string)
  }))

  default = [
    {
      userarn  = "arn:aws:iam::411543714039:user/terra"
      username = "terra"
      groups   = ["system:masters"]
    },

  ]
}
