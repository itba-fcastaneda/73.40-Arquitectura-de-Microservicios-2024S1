git clone https://github.com/nginxinc/kubernetes-ingress.git --branch v3.4.3
kubectl apply -f kubernetes-ingress/deployments/common/ns-and-sa.yaml
kubectl apply -f kubernetes-ingress/deployments/rbac/rbac.yaml
kubectl apply -f kubernetes-ingress/deployments/common/nginx-config.yaml
kubectl apply -f kubernetes-ingress/deployments/common/ingress-class.yaml
kubectl apply -f kubernetes-ingress/deployments/deployment/nginx-ingress.yaml
kubectl apply -f https://raw.githubusercontent.com/nginxinc/kubernetes-ingress/v3.4.3/deploy/crds.yaml
kubectl scale --replicas=2 deployment/nginx-ingress -n nginx-ingress
kubectl create -f kubernetes-ingress/deployments/service/nodeport.yaml
